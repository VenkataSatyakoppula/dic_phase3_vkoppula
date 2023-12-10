from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import datetime,os,shutil
import cleaning,eda,ml_models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload_data/{name}",response_model=schemas.DataSetCreate)
async def upload_dataset(name:str,file: UploadFile = File(),db: Session = Depends(get_db)):
    
    exists = crud.get_dataset(db=db,name=name)
    if exists:
         raise HTTPException(status_code=400, detail="Dataset with this name already exists")
    file_location = os.path.join(os.getcwd(),f"data-sets/{name}.csv")
    created = crud.create_dataset(db=db,name=name,file_path=file_location)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return created

@app.delete("/delete_data/{name}")
async def delete(name:str,db: Session = Depends(get_db)):
    deleted  = crud.delete_dataset(db=db,name=name)
    if deleted:
        return {"status":"File Deleted!"}
    raise HTTPException(status_code=400, detail="Dataset Doesn't exists")

@app.get("/list_all/",response_model=List[schemas.Dataset])
async def list_all(db: Session = Depends(get_db)):
    all_records  = crud.list_all(db=db)
    return all_records

@app.get("/list/{name}/",response_model=schemas.Dataset)
async def list_specific(name: str,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if not exists:
        raise HTTPException(status_code=400, detail="Dataset Doesn't exists")
    return exists

@app.get("/get_columns/{name}")
async def get_columns(name:str,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if not exists:
        raise HTTPException(status_code=400, detail="Dataset Doesn't exists")
    columns = cleaning.get_columns(exists.file_path)
    return columns.to_list()

@app.get("/get_num_columns/{name}")
async def get_num_columns(name:str,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if not exists:
        raise HTTPException(status_code=400, detail="Dataset Doesn't exists")
    columns = cleaning.get_columns(exists.file_path,type="num")
    return columns.to_list()

@app.get("/get_cat_columns/{name}")
async def get_cat_columns(name:str,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if not exists:
        raise HTTPException(status_code=400, detail="Dataset Doesn't exists")
    columns = cleaning.get_columns(exists.file_path)
    num_columns = cleaning.get_columns(exists.file_path,type="num")
    cat_cols = [item for item in columns.to_list() if item not in num_columns.to_list()]
    return cat_cols


@app.get("/get_head/{name}")
async def get_heads(name:str,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if not exists:
        raise HTTPException(status_code=400, detail="Dataset Doesn't exists")
    head = cleaning.get_head(exists.file_path)
    return Response(head)

@app.post("/clean/{name}/{step}/")
async def cleaning_step(step:int,name:str,data:schemas.DatasetBody,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if exists:
        # current_step = exists.cleaning_step+1
        # crud.update_clean_step(db=db,name=name,clean_step=current_step)
        match(step):
            case 1:
                response = cleaning.get_missing_data(exists.file_path)
                # response["step"] = current_step
                return JSONResponse(response)
            case 2:
                response = cleaning.remove_null(exists.file_path)
                # response["step"] = current_step
                return JSONResponse(response)
            case 3:
                cleaning.remove_duplicate(exists.file_path)
                return {"status":"Duplicates are removed!"}
            case 4:
                drop_columns = data.columns
                response =  cleaning.drop_cols(exists.file_path,columns=drop_columns)  
                # response["step"] = current_step
                return JSONResponse(response)
            case 5:
                response = cleaning.imputation_of_missing_values(exists.file_path)  
                # response["step"] = current_step
                return JSONResponse(response)  
            case 6:
                response = cleaning.get_datatypes(exists.file_path)
                # response["step"] = current_step
                return JSONResponse(response)  
            case 7:
                rename_columns = data.rename
                response = cleaning.renaming_columns(exists.file_path,rename_columns)   
                # response["step"] = current_step
                return JSONResponse(response) 
            case 8:
                numerical_columns = data.columns
                response = cleaning.data_trimming(exists.file_path,numerical_columns)   
                # response["step"] = current_step
                return Response(response) 
            case 9:
                response = cleaning.describe_data(exists.file_path)   
                # response["step"] = current_step
                return JSONResponse(response) 
            case 10:
                numerical_columns = data.columns
                response = cleaning.box_blot_outliers(exists.file_path,numerical_columns)   
                # response["step"] = current_step
                return JSONResponse(response)
            case _:
                raise HTTPException(status_code=400, detail="something went wrong")
    raise HTTPException(status_code=400, detail="Dataset Doesn't exists or cleaning not started yet")    


@app.post("/eda/{name}/{step}/")
async def eda_step(step:int,name:str,data:schemas.DatasetBody,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if exists:
        match(step):
            case 1:
                column = data.columns[0]
                response =  eda.histogram(exists.file_path,column)
                return JSONResponse(response)
            case 2:
                columns = data.columns
                response =  eda.analysis_mean_by(filename=exists.file_path,numeric_col=columns[0],cat_col=columns[1])
                return JSONResponse(response)
            case 3:
                columns = data.columns
                response =  eda.count_plot(filename=exists.file_path,col1=columns[0],col2=columns[1])
                return JSONResponse(response)
            case 4:
                columns = data.columns
                response =  eda.heat_map(filename=exists.file_path,columns_of_interest=columns)
                return JSONResponse(response)
            case 5:
                columns = data.columns
                response =  eda.density_graph(filename=exists.file_path,col1=columns[0],col2_numeric=columns[1])
                return JSONResponse(response)
            case 6:
                columns = data.columns
                response =  eda.piechart(filename=exists.file_path,col=columns[0])
                return JSONResponse(response)
            case 7:
                columns = data.columns
                response =  eda.scatter_plot(filename=exists.file_path,col1=columns[0],col2_numeric=columns[1],col3_numeric=columns[2])
                return JSONResponse(response)
            case 8:
                columns = data.columns
                response =  eda.cross_tab(filename=exists.file_path,col1=columns[0],col2=columns[1],col3=columns[2])
                return JSONResponse(response)
            case _:
                raise HTTPException(status_code=400, detail="Something went wrong")
    raise HTTPException(status_code=400, detail="Dataset Doesn't exists or cleaning not started yet")    


@app.post("/model/{name}/{step}/")
async def run_model(step:int,name:str,data:schemas.DatasetBody,db: Session = Depends(get_db)):
    exists = crud.get_dataset(db=db,name=name)
    if exists:
        match(step):
            case 1:
                k_value = data.values["k"]
                response =  ml_models.KNN_algo(exists.file_path,int(k_value))
                return JSONResponse(response)
            case 2:
                response =  ml_models.lgr_algo(exists.file_path)
                return JSONResponse(response)
            case 3:
                n_value = data.values["n_value"]
                response =  ml_models.random_forest_algo(exists.file_path,n_value=int(n_value))
                return JSONResponse(response)
            case 4:
                response =  ml_models.svc_rbf_kernal(exists.file_path)
                return JSONResponse(response)
            case 5:
                n_estimators = data.values["n_estimators"]
                max_depth = data.values["max_depth"]
                response =  ml_models.xgboost_classifier(exists.file_path,int(n_estimators),int(max_depth))
                return JSONResponse(response)
            case 6:
                response =  ml_models.gaussian_classifier(exists.file_path)
                return JSONResponse(response)
            case _:
                raise HTTPException(status_code=400, detail="Something went wrong")
    raise HTTPException(status_code=400, detail="Dataset Doesn't exists or cleaning not started yet")    

@app.get("/")
async def index():
    return datetime.datetime.now()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
