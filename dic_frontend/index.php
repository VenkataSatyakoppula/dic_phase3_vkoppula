<?php
include 'helper/header.php';
?>
<body>
<!-- modal for adding a dataset -->
<div class="modal fade" id="addDataset" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="addDataset">Add Dataset</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form id="add-dataset" enctype="multipart/form-data">
          <div class="mb-3">
            <label for="recipient-name" class="col-form-label">Name(should be unique):</label>
            <input type="text" class="form-control" name="name">
          </div>
          <div class="mb-3">
            <label for="message-text" class="col-form-label">Datset:</label>
            <input type="file" name="file">
          </div>
        </form>
      </div>
      <div class="modal-footer" id="upload-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="submit" class="btn btn-success" id="add-dataset-submit">Create</button>
      </div>
    </div>
  </div>
</div>

<div  class="contianer">
    <h3 class="mb-5"></h3>
    <h4>Your Datasets <button class="btn btn-success mx-3" data-bs-toggle="modal" data-bs-target="#addDataset">Add a Dataset</button> </h4> 
    
    <div class="d-flex m-3 flex-wrap" id="all-datasets">
    <a href="#" class="list-group-item list-group-item-action mb-3" aria-current="true">
        <div class="d-flex w-100 justify-content-between">
        <h5 class="mb-1">List group item heading</h5>
        <small>3 days ago</small>
        <button class="btn btn-danger">Delete</button>
        </div>
    </a>
    <a href="#" class="list-group-item list-group-item-action">
        <div class="d-flex w-100 justify-content-between">
        <h5 class="mb-1">List group item heading</h5>
        <small class="text-body-secondary">3 days ago</small>
        <button class="btn btn-danger">Delete</button>
        </div>
    </a>

</div>
</div>
  </div>
<?php include 'helper/footer.php'; ?>

<script>
    $(document).ready(function() {
        LoadData();
    });
</script>