<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EDA Page</title>
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
<div class="container">
<h1 class="my-5 text-center"><button class="btn btn-danger back" onclick="redirectToPage('single.php')">Back</button> EDA Graphs</h1>
    
    <h2 class="mb-2">Dataset name:  <?php echo $_GET["name"] ?> </h2>
    <!-- 10 h5 elements with empty spaces -->
    <div class="container">
        <h5>Histogram         
        <select class="form-select single_columns histogram">
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
        </select></h5> 

        <div id="histogram"></div>
        <h5>analysis_mean  (numeric col,categorical col)
                <span class="d-flex">
                <select class="form-select single_columns_num analysis_mean1 mx-1">  </select> BY
                <select class="form-select single_cat_columns analysis_mean2" > </select>
    </span>
                <!-- <select class="form-select all_columns analysis_mean" multiple></select> -->
        </h5>
        <div id="analysis_mean">
        </div> 

        <h5>count_plot  any (col1,col2) 
        <span class="d-flex">
                <select class="form-select single_columns count_plot1 mx-1">  </select> BY
                <select class="form-select single_columns count_plot2" > </select>
    </span>
        </h5>
        <div id="count_plot"></div> 

        <h5>heat_map select any columns<select class="form-select single_columns_num heat_map" multiple></select></h5>
        <div id="heat_map"></div>   

        <h5>density_graph (categorical col,numeric col) 
        <span class="d-flex">
                <select class="form-select single_cat_columns density_graph1 mx-1">  </select> BY
                <select class="form-select single_columns_num density_graph2" > </select>
    </span>
        </h5>
        <div id="density_graph"></div>     

        <h5>piechart   <select class="form-select single_cat_columns piechart">
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
        </select> </h5>
        <div id="piechart"></div>   

        <h5>scatter_plot (categorical col,numeric col1,numeric col2)
        <span class="d-flex">
        <select class="form-select single_cat_columns scatter_plot1 mx-1">  </select> BY
                <select class="form-select single_columns_num scatter_plot2" > </select> BY
                <select class="form-select single_columns_num scatter_plot3 mx-1">  </select> 
        </span >
            </h5>
        <div id="scatter_plot"></div>   

        <h5>cross_tab any three cols <select class="form-select all_columns cross_tab" multiple></select></h5>
        <div id="cross_tab"></div>        
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
        get_columns();
        get_num_colmns();
        get_cat_colmns();

    })
    let dataset = "<?php echo $_GET["name"]?>";
    function redirectToPage(page) {
        window.location.href = page+`?name=${dataset}`;
    }
</script>
</html>
