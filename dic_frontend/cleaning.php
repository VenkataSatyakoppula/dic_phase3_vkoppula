<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cleaning Page</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.css" integrity="sha512-3pIirOrwegjM6erE5gPSwkUzO+3cTjpnV9lexlNZqvupR64iZBnOOTiiLPb9M36zpMScbmUNIcHUqKD47M719g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    
    <style>
        h5 {
            margin-top: 2rem;
        } 
        img{
            height: 25rem;
            width: 25rem;
        }
        th,td{
            border: 1px solid black;
        }
    </style>
</head>
<body>
<!-- cleaning Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Select columns</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
      <label for="columnNames">Choose columns:</label>
        <form id="columns">
        

        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary clean_submit">Save changes</button>
      </div>
    </div>
  </div>
</div>
<!-- rename modal -->
<div class="modal fade" id="rename_modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Select columns to remove</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div>
            Column names: <span id="columns2"></span>
        </div>
      <label for="columnNames">Rename columns:</label>
        <form id="rename_col">
        <div class="input-group rename-group mb-2">
        <input class="mx-2" type="text" name="oldName[]" placeholder="Old Name"> <br>
        <input type="text" name="newName[]" placeholder="New Name">
        </div>
        </form>
        <button class="btn btn-primary addinputs">Add</button>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary clean7_submit">Save changes</button>
      </div>
    </div>
  </div>
</div>
<div class="container">
<h1 class="my-5 text-center"><button class="btn btn-danger back" onclick="redirectToPage('single.php')">Back</button> Cleaning steps</h1>
    
    <h2 class="mb-2">Dataset name:  <?php echo $_GET["name"] ?> </h2>
    <!-- 10 h5 elements with empty spaces -->
    <h5>1. Get Missing Data <button class="btn btn-primary" id="clean_1"> <i class="fa-solid fa-play"></i> Run</button></h5>
    <div class="container mb-2" id="missing_data">
        
    </div>

    <h5>2. Remove null values <button class="btn btn-primary" id="clean_2"> <i class="fa-solid fa-play"></i> Run</button></h5>
    <div class="container mb-2" id="remove_null">
        
    </div>   
    <h5>3. Remove duplicates <button class="btn btn-primary" id="clean_3"> <i class="fa-solid fa-play"></i> Run</button></h5>
    <div class="container mb-2" id="remove_duplicates">
        
    </div>    
    <h5>4. Drop Columns <button class="btn btn-primary" id="clean_4"> <i class="fa-solid fa-play"></i> Run</button></h5>
    <div class="container mb-2" id="drop_columns">
        
    </div>     
    <h5>5. Impute Missing values <button class="btn btn-primary" id="clean_5"> <i class="fa-solid fa-play"></i> Run</button></h5>
    <div class="container mb-2" id="impute">
        
        </div>    
    <h5>6. Get Datatypes <button class="btn btn-primary" id="clean_6"> <i class="fa-solid fa-play"></i> Run</button></h5>

    <div class="container mb-2" id="get_datatypes">
        
    </div>   
     <h5>7. Re-naming columns <button class="btn btn-primary" id="clean_7"> <i class="fa-solid fa-play"></i> Run</button></h5>
    <div class="container mb-2" id="renaming_columns">
        
    </div>    
    <h5>8. Data Trimming  <button class="btn btn-primary" id="clean_8"> <i class="fa-solid fa-play"></i> Run</button> (Select only numerical columns)</h5>
    <div class="container mb-2" id="data_trimming">
        
    </div>    
    <h5>9. Describe data <button class="btn btn-primary" id="clean_9"> <i class="fa-solid fa-play"></i> Run</button></h5>
    <div class="container mb-2" id="describe_data">
        
    </div>  
    <h5>10. Remove Outliers and Box plot <button class="btn btn-primary" id="clean_10"> <i class="fa-solid fa-play"></i> Run</button> (Select only numerical columns)</h5>
    <div class="container mb-2" id="outliers">
        
    </div> 
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js" integrity="sha512-VEd+nq25CkR676O+pLBnDW09R7VQX9Mdiij052gVCp5yVH3jGtH70Ho/UUv4mJDsEdTvqRCFZg0NKGiojGnUCw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script> 
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.3/jquery.min.js" integrity="sha512-STof4xm1wgkfm7heWqFJVn58Hm3EtS31XFaagaa8VMReCXAkQnJZ+jEy8PCC/iT18dFy95WcExNHFTqLyp72eQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.5/jquery.validate.min.js" integrity="sha512-rstIgDs0xPgmG6RX1Aba4KV5cWJbAMcvRCVmglpam9SoHZiUCyQVDdH2LPlxoHtrv17XWblE/V/PP+Tr04hbtA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js" integrity="sha512-VEd+nq25CkR676O+pLBnDW09R7VQX9Mdiij052gVCp5yVH3jGtH70Ho/UUv4mJDsEdTvqRCFZg0NKGiojGnUCw==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
</body>
<script type="text/javascript"  src="js/main.js">
    var dataset = "<?php echo $_GET["name"]?>";

    
</script>
<script>
    $( document ).ready(function() {
        //blur_cleaning();
        // LoadData();
    })
    let dataset = "<?php echo $_GET["name"]?>";
    function redirectToPage(page) {
        window.location.href = page+`?name=${dataset}`;
    }
</script>
</html>
