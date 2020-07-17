function deletedata(id, section){
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#34c38f",
      cancelButtonColor: "#f46a6a",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
        if (result.value) {
        $.ajax({
            type: "DELETE",
            url: "delete/"+section+"/"+id,
            dataType: "json",
            beforeSend: function() {  },
            success: (response) => {
                console.log(response)
                Swal.fire("Deleted!", "Your file has been deleted.", "success");
            },
            error: (error) => {
                Swal.fire("Not Deleted!", "Something went wrong", "error");
            },
            complete: () => {
                setTimeout(() => {
                    location.reload()
                }, 2000);
            },
        });
    }
    });
}
