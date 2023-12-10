$( document ).ready(function() {
    let backend_url = "http://127.0.0.1:8000";
    let columns,num_col,cat_col;
    var selectionOrder = []
    
    function UploadFile(formData){
        $.ajax({
            url: `${backend_url}/upload_data/${formData.get("name")}`,
            type: 'POST',
            data: formData,
            processData: false, // Prevents jQuery from converting the FormData object into a string
            contentType: false, // Prevents jQuery from setting the Content-Type header
            success: function(response) {
                $("#upload-footer").html("Uploaded Sucessfully!");
                setTimeout(()=>{
                    location.reload()
                }, 2000);
            },
            error: function(response) {
                console.log('Error during file upload');
                console.log(response);
            }
        });
    }
    function LoadData(){
        var settings = {
            "url": `${backend_url}/list_all/`,
            "method": "GET",
            "timeout": 0,
          };
          
          $.ajax(settings).done(function (response) {
            let html = ""
            response.forEach(function(item) {
                var date = new Date(item.created_on)
                html += `<div class="card m-1" style="width: 12rem; ">
                <img src="https://t4.ftcdn.net/jpg/04/75/03/07/360_F_475030738_kT8sJumBrd5E3cPDhzn0nWjHsGuP79u9.jpg" class="card-img-top" alt="dataset">
                <div class="card-body">
                  <h5 class="card-title">${item.name}</h5>
                  <p class="card-text">Date created: ${date.toLocaleDateString()}.</p>
                  <p class="card-text">Time: ${date.toLocaleTimeString()}.</p>
                  <div class="d-flex justify-content-center">
                  <a href="single.php?name=${item.name}" class="btn btn-primary w-100">start</a>
                  
                  </div>
                  <button class="btn btn-danger w-100 mt-1" onclick="DeleteData('${item.name}')">Delete</button>
                </div>
              </div>`
            });
            $("#all-datasets").html(html)
          });
    }
    function get_columns(){
        var settings = {
            "url": `${backend_url}/get_columns/${dataset}`,
            "method": "GET",
            "timeout": 0,
          };
          
          $.ajax(settings).done(function (response) {
            html = `<select class = "form-select form-select-sm" name="columnNames" id="columnNames" multiple>`
            html2 = `<br>`
            html3 = ``
           
            for(let i=0;i<response.length;i++){
                html+= `<option value="${response[i]}">${response[i]}</option>`
                html2 += `${response[i]} <br>`
                html3 += `<option value="${response[i]}">${response[i]}</option>`
            }
            html += "</select>"
            $("#columns").html(html)
            $("#columns2").html(html2)
            $(".all_columns").html(html3)
            $(".single_columns").html(html3)
            columns = response
          });
          
    }
    function get_num_colmns() {
        var settings = {
            "url": `${backend_url}/get_num_columns/${dataset}`,
            "method": "GET",
            "timeout": 0,
          };
          
          $.ajax(settings).done(function (response) {
            html = ``
           
            for(let i=0;i<response.length;i++){
                html+= `<option value="${response[i]}">${response[i]}</option>`
            }
            html += "</select>"
            $(".single_columns_num").html(html)
            num_col = response
          });
    }
    function get_cat_colmns() {
        var settings = {
            "url": `${backend_url}/get_cat_columns/${dataset}`,
            "method": "GET",
            "timeout": 0,
          };
          
          $.ajax(settings).done(function (response) {
            html = ``
           
            for(let i=0;i<response.length;i++){
                html+= `<option value="${response[i]}">${response[i]}</option>`
            }
            html += "</select>"
            $(".single_cat_columns").html(html)
            cat_col = response
          });
    }
    window.get_columns = get_columns;
    window.get_num_colmns = get_num_colmns;
    window.get_cat_colmns = get_cat_colmns;
    function DeleteData(dataset_name) {
        var settings = {
        "url": `${backend_url}/delete_data/${dataset_name}`,
        "method": "DELETE",
        "timeout": 0,
        "processData": false,
        "contentType": false,
        };

        $.ajax(settings).done(function (response) {
            toastr.success(`${dataset_name} Deleted!`);
            LoadData();
        });
    }
    window.DeleteData = DeleteData;
    function cleaning(step,data){
        var settings = {
            "url": `${backend_url}/clean/${dataset}/${step}/`,
            "method": "POST",
            "timeout": 0,
            "headers": {
              "Content-Type": "application/json"
            },
            "data": JSON.stringify(data),
          };
          
          $.ajax(settings).done(function (res) {
            switch(step){
                case 1:
                    html = "<div class='d-flex align-items-center'><div><strong>Total Missing Values</strong> <br>"
                    for (var key in res.missing_data) {
                         
                        for (var subKey in res.missing_data[key]) {
                            html += `<span>${subKey + ':' + res.missing_data[key][subKey]} </span> <br>`
                        }
                        break;
                    }
                    html += `</div><img src="data:image/png;base64,${res.plot_image}" class ="img-fluid"> </div>`
                    $("#missing_data").html(html)
                    break;
                case 2:
                    html = "<strong>Total Null Values</strong> <br>"
                    for (const key in res) {
                        if (res.hasOwnProperty(key)) {
                            html += `<span>${key + ': ' + res[key]} </span> <br>`
                        }
                    }
                    $("#remove_null").html(html)
                    break;
                case 3:
                    html = "<strong>Duplicates are removed!</strong>"
                    $("#remove_duplicates").html(html)
                    break;
                case 4:
                    console.log("hello")
                    html = `<strong>${res.status}<strong>`
                    $("#drop_columns").html(html)
                    break;
                case 5:
                    html = `<strong>Missing Values are Imputated Successflly!<strong>`
                    $("#impute").html(html)
                    break;
                case 6:
                    html = "<strong>Column Datatypes</strong> <br>"
                    for (const key in res) {
                        if (res.hasOwnProperty(key)) {
                            html += `<span>${key + ': ' + res[key]} </span> <br>`
                        }
                    }
                    $("#get_datatypes").html(html)
                    break;
                case 7:
                    html = "<strong>Renamed Columns</strong> <br>"
                    for (const key in res) {
                        if (res.hasOwnProperty(key)) {
                            html += `<span>${key + ': ' + res[key]} </span> <br>`
                        }
                    }
                    $("#renaming_columns").html(html)
                    break;
                case 8:
                    html = "<strong>Dataframe head after trimming</strong> <br>"

                    $("#data_trimming").html(html+res)
                    break;
                case 9:
                    html = "<strong>Data Description</strong> <br>"

                    $("#describe_data").html(html+res)
                    break;
                case 10:
                    html = "<div class='d-flex align-items-center'><div><strong>Outliers</strong> <br>"
                    for (var key in res.outliers) {
                         
                        html += `<span>${key + ':' + res.outliers[key]} </span> <br>`

                    }
                    html += `</div><img  src="data:image/png;base64,${res.boxplot_image}" class ="img-fluid"> </div>`
                    $("#outliers").html(html)
                    break;
            }
          });
    }
    function EDA_Graphs(step,data) { 
        var settings = {
            "url": `${backend_url}/eda/${dataset}/${step}/`,
            "method": "POST",
            "timeout": 0,
            "headers": {
              "Content-Type": "application/json"
            },
            "data": JSON.stringify(data),
          };
          
          $.ajax(settings).done(function (res) {
            switch(step){
                case 1:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#histogram").html(html)
                    break;
                
                case 2:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#analysis_mean").html(html)
                    break;
                case 3:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#count_plot").html(html)
                    break;
                case 4:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#heat_map").html(html)
                    break;
                case 5:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#density_graph").html(html)
                    break;
                case 6:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#piechart").html(html)
                    break;
                case 7:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#scatter_plot").html(html)
                    break;
                case 8:
                    html = `<img src="data:image/png;base64,${res.plot}" class ="img-fluid">`
                    $("#cross_tab").html(html)
                    break;
                }
          });
     }
     function RunModals(step,data) { 
        var settings = {
            "url": `${backend_url}/model/${dataset}/${step}/`,
            "method": "POST",
            "timeout": 0,
            "headers": {
              "Content-Type": "application/json"
            },
            "data": JSON.stringify(data),
          };
          
          $.ajax(settings).done(function (res) {
            switch(step){
                case 1:
                    html = `<div> Train Accuracy:<strong style="color:red"> ${res.train_accuracy} %</strong> <br>Test Accuracy: <strong style="color:red"> ${res.test_accuracy}%</strong> </div>`
                    html += res.html_report
                    html += `<div><img src="data:image/png;base64,${res.confusion_matrix}" class ="img-fluid"></div>`
                    html += `<div><img src="data:image/png;base64,${res.PR_curve}" class ="img-fluid"></div>`
                    html += `<div><img src="data:image/png;base64,${res.k_curve}" class ="img-fluid"></div>`
                    $("#knn_output").html(html)
                    break;
                case 2:
                    html = `<div> Train Accuracy:<strong style="color:red"> ${res.train_accuracy} %</strong> <br>Test Accuracy: <strong style="color:red"> ${res.test_accuracy}%</strong> </div>`
                    html += res.html_report
                    html += `<div><img src="data:image/png;base64,${res.confusion_matrix}" class ="img-fluid"></div>`
                    html += `<div><img src="data:image/png;base64,${res.PR_curve}" class ="img-fluid"></div>`
                    $("#lgr_output").html(html)
                    break;
                case 3:
                    html = `<div> Train Accuracy:<strong style="color:red"> ${res.train_accuracy} %</strong> <br>Test Accuracy: <strong style="color:red"> ${res.test_accuracy}%</strong> </div>`
                    html += res.html_report
                    html += `<div><img src="data:image/png;base64,${res.confusion_matrix}" class ="img-fluid"></div>`
                    html += `<div><img src="data:image/png;base64,${res.PR_curve}" class ="img-fluid"></div>`
                    $("#rf_output").html(html)
                    break;
                case 4:
                    html = `<div> Train Accuracy:<strong style="color:red"> ${res.train_accuracy} %</strong> <br>Test Accuracy: <strong style="color:red"> ${res.test_accuracy}%</strong> </div>`
                    html += res.html_report
                    html += `<div><img src="data:image/png;base64,${res.confusion_matrix}" class ="img-fluid"></div>`
                    html += `<div><img src="data:image/png;base64,${res.PR_curve}" class ="img-fluid"></div>`
                    $("#svc_output").html(html)
                    break;
                case 5:
                    html = `<div> Train Accuracy:<strong style="color:red"> ${res.train_accuracy} %</strong> <br>Test Accuracy: <strong style="color:red"> ${res.test_accuracy}%</strong> </div>`
                    html += res.html_report
                    html += `<div><img src="data:image/png;base64,${res.confusion_matrix}" class ="img-fluid"></div>`
                    html += `<div><img src="data:image/png;base64,${res.PR_curve}" class ="img-fluid"></div>`
                    $("#xgb_output").html(html)
                    break;
                case 6:
                    html = `<div> Train Accuracy:<strong style="color:red"> ${res.train_accuracy} %</strong> <br>Test Accuracy: <strong style="color:red"> ${res.test_accuracy}%</strong> </div>`
                    html += res.html_report
                    html += `<div><img src="data:image/png;base64,${res.confusion_matrix}" class ="img-fluid"></div>`
                    html += `<div><img src="data:image/png;base64,${res.PR_curve}" class ="img-fluid"></div>`
                    $("#gauss_output").html(html)
                    break;
            }
            
          });
     }
    window.LoadData = LoadData;
    $('#add-dataset').submit(function(e){ e.preventDefault(); }).validate({
        rules:{
            name: {
                required: true,
                minlength: 2
            },
            file: {
                required: true,
            }
        },
        messages: {
            name: {
                required: 'Please enter your Dataset name'
            },
            file: {
                required: 'Please upload the dataset'
            }
        },
        errorPlacement: function(error, element) {
              error.insertAfter(element).css("color","red");
        },
        submitHandler: function (form) {
            var formData = new FormData(form);
            UploadFile(formData);
            $(form).find('input').attr('disabled', true).css('opacity',0.5);
            return false;
        }
    });
    $('#columns').submit(function(e){ e.preventDefault(); }).validate({
        submitHandler: function (form) {
            var formData = new FormData(form);
            var values = [];
            for (var pair of formData.entries()) {
                values.push(pair[1]); // pair[0] is the key, pair[1] is the value
            }

            let step = $(".clean_submit").attr("data-id");
        
            cleaning(parseInt(step),{"columns":values})
            $(form).find('input').attr('disabled', true).css('opacity',0.5);
            return false;
        }
    });
    $('#rename_col').submit(function(e){ e.preventDefault(); }).validate({
        submitHandler: function (form) {
            var formData = new FormData(form);
            const oldNames = formData.getAll('oldName[]');
            const newNames = formData.getAll('newName[]');
            
            let renameMapping = {};
            oldNames.forEach((oldName, index) => {
                if (oldName && newNames[index]) { // Ensure both old and new names are provided
                    renameMapping[oldName] = newNames[index];
                }
            });
        
            console.log(renameMapping);

            let step = $(".clean7_submit").attr("data-id");
        
            cleaning(parseInt(step),{"rename":renameMapping})
            return false;
        }
    });
    
    //event listeners
    $("body").on('click','#add-dataset-submit', function() {
        $('#add-dataset').submit();
    });
    $("body").on('click','#clean_1', function() {
        cleaning(1,{})
    });
    $("body").on('click','#clean_2', function() {
        cleaning(2,{})
    });
    $("body").on('click','#clean_3', function() {
        cleaning(3,{})
    });    
    $("body").on('click','#clean_4', function() {
        $("#exampleModal").modal("show");
        $(".clean_submit").attr("data-id",4)
        get_columns();
    });    
    $("body").on('click','#clean_5', function() {
        cleaning(5,{})
    });    
    $("body").on('click','#clean_6', function() {
        cleaning(6,{})
    });    
    $("body").on('click','#clean_7', function() {
        $("#rename_modal").modal("show");
        $(".clean7_submit").attr("data-id",7);
        get_columns();
        
    });    
    $("body").on('click','#clean_8', function() {
        $("#exampleModal").modal("show");
        $(".clean_submit").attr("data-id",8)
        get_columns();
    });    
    $("body").on('click','#clean_9', function() {
        cleaning(9,{})
    });
    $("body").on('click','#clean_10', function() {
        $("#exampleModal").modal("show");
        $(".clean_submit").attr("data-id",10)
        get_columns();
    });
    
    
    
    // modal submits
    $("body").on('click','.clean_submit', function() {
        $('#columns').submit();
        $("#exampleModal").modal("hide");
    });
    $("body").on('click','.clean7_submit', function() {
        $('#rename_col').submit();
        $("#rename_modal").modal("hide");
    });
    $("body").on('click','.addinputs', function() {
        var inputs = '<input class="mx-2" type="text" name="oldName[]" placeholder="Old Name"> <br><input type="text" name="newName[]" placeholder="New Name">'
        $('.input-group').append(inputs);
    });
    // eda
    $("body").on('click','.histogram', function() {
        var selectedValue =  $('.histogram').find('option:selected').map(function() {
            return this.value;
        }).get();
        EDA_Graphs(1,{"columns":selectedValue})
    });

    $("body").on('click','.analysis_mean1,.analysis_mean2', function() {
        var selectedValue =  $(".analysis_mean1").val();
        var selectedValue2 =  $(".analysis_mean2").val();
        let selected = [selectedValue,selectedValue2]
  
        EDA_Graphs(2,{"columns":selected})
    });

    $("body").on('click','.count_plot1,count_plot2', function() {
        var selectedValue =  $(".count_plot1").val();
        var selectedValue2 =  $(".count_plot2").val();
        let selected = [selectedValue,selectedValue2]

        EDA_Graphs(3,{"columns":selected})
    });

    $("body").on('click','.heat_map', function() {
        var selectedValues = $('.heat_map').val();
      
        EDA_Graphs(4,{"columns":selectedValues})
    });
    $("body").on('click','.density_graph1,.density_graph2', function() {
        var selectedValue = $('.density_graph1').val();
        var selectedValue2 = $('.density_graph2').val();
        let selected = [selectedValue,selectedValue2]
       
        EDA_Graphs(5,{"columns":selected})
    });
    $("body").on('click','.piechart', function() {
        var selectedValues = $('.piechart').val();
        console.log(selectedValues); 
        EDA_Graphs(6,{"columns":[selectedValues]})
    });
    $("body").on('click','.scatter_plot1,.scatter_plot2,.scatter_plot3', function() {
        var selectedValue1 = $('.scatter_plot1').val();
        var selectedValue2 = $('.scatter_plot2').val();
        var selectedValue3 = $('.scatter_plot3').val();
        let selected = [selectedValue1,selectedValue2,selectedValue3]
        EDA_Graphs(7,{"columns":selected})
    });
    $("body").on('click','.cross_tab', function() {
        var selectedValues = $('.cross_tab').val();
        if( selectedValues.length != 3){
            toastr.warning("Select 3 columns!")
        }else{
            EDA_Graphs(8,{"columns":selectedValues})
        }

    });

    // modal performance
    $("body").on('click','.knn', function() {
        let k = $("#k_value").val()
        RunModals(1,{"values":{"k":k}})

    });
    $("body").on('click','.lgr', function() {
        RunModals(2,{"values":{}})
    });
    $("body").on('click','.rf', function() {
        let n = $("#n_value").val()
        RunModals(3,{"values":{"n_value":n}})
    });
    $("body").on('click','.svc', function() {
        RunModals(4,{"values":{}})
    });
    $("body").on('click','.xgb', function() {
        let n = $("#n_estimators").val()
        let max_depth = $("#max_depth").val()
        RunModals(5,{"values":{"n_estimators":n,"max_depth":max_depth}})
    });
    $("body").on('click','.gauss', function() {
        RunModals(6,{"values":{}})
    });


});