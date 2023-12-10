<?php
include 'helper/header.php';

?>

<body>
<style>


        .btn-container {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .header{
            text-align: center;
        }


        button {
            width: 50vh;
            height: 20vh;
            font-size: 100px;
            margin: 4%;
        }
        #exclude{
            width: 10%;
            height: 10%;
        }
    </style>

    <div class="header mt-5">
        <h1>Welcome to the Home Page </h1>
        <button class="btn btn-danger" id="exclude" onclick="redirectToPage('index.php')" >back</button>
    </div>
    

    <div class="btn-container">
        <div class="btn-group">
            <button class="btn btn-primary" onclick="redirectToPage('cleaning.php')">Go to Cleaning</button>
        </div>

        <div class="btn-group">
            <button class="btn btn-success" onclick="redirectToPage('eda.php')">Go to EDA</button>
        </div>

        <div class="btn-group">
            <button class="btn btn-warning" onclick="redirectToPage('model.php')">Model performance</button>
        </div>
    </div>

    </div>

<?php include 'helper/footer.php'; ?>

<script>
    var dataset = "<?php echo $_GET["name"]?>";
    function redirectToPage(page) {
        window.location.href = page+`?name=${dataset}`;
    }
</script>