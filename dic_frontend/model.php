<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Model performance Page</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css" integrity="sha512-MV7K8+y+gLIBoVD59lQIYicR65iaqukzvf/nwasF0nqhPay5w/9lJmVM2hMDcnK1OnMGCdVK+iQrJ7lzPJQd1w==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.css" integrity="sha512-3pIirOrwegjM6erE5gPSwkUzO+3cTjpnV9lexlNZqvupR64iZBnOOTiiLPb9M36zpMScbmUNIcHUqKD47M719g==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    
    <style>
        h5 {
            margin-top: 2rem;
        } 
        img{
            height: 35rem;
            width: 35rem;
        }
        th,td{
            border: 1px solid black;
        }

    </style>
</head>
<body>
<div class="container">
<h1 class="my-5 text-center"><button class="btn btn-danger back" onclick="redirectToPage('single.php')">Back</button> Model Performance</h1>
    
    <h2 class="mb-2">Dataset name:  <?php echo $_GET["name"] ?> </h2>
    <!-- 10 h5 elements with empty spaces -->
    <div class="container">
        <h5>KNN <br> <input class="mr-2" type="number" name="k_value" id="k_value" placeholder="k-value(ex=5)" ><button class="btn btn-success knn"> <i class="fa-solid fa-play"></i> Predict</button>
        </h5>
        <div  id="knn_output"></div>
        <h5>Logistic Regression <button class="btn btn-success lgr"> <i class="fa-solid fa-play"></i> Predict</button></h5>
        <div id="lgr_output"></div>
        <h5>Random forest classifier <br> <input class="mr-2" type="number" name="n_value" id="n_value" placeholder="n-estimators(ex=5)" ><button class="btn btn-success rf"> <i class="fa-solid fa-play"></i> Predict</button></h5>
        <div id="rf_output"></div>
        <h5>SVC with rbf kernal <button class="btn btn-success svc"><i class="fa-solid fa-play"></i> Predict</button></h5>  
        <div id="svc_output"></div>
        <h5>xgboostClassifier <br>
            <input class="mr-2" type="number" name="n_estimators" id="n_estimators" placeholder="n_estimators(ex=100)" >
            <input class="mr-2" type="number" name="max_depth" id="max_depth" placeholder="max_depth(ex=5)" ><button class="btn btn-success xgb"><i class="fa-solid fa-play"></i> Predict</button>

        </h5>
        <div id="xgb_output"></div>
        <h5>Gaussian Naive Bayes <button class="btn btn-success gauss"><i class="fa-solid fa-play"></i> Predict</button></h5>  
        <div id="gauss_output"></div>
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
