
    $("#SelectCategory").change(function () {
        const url = $("#formCategory").attr("data-brands-category-url");  // get the url of the `load_cities` view
        const categoryName = $(this).val();  // get the selected country ID from the HTML input

        $.ajax({                       // initialize an AJAX request
            url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
            data: {
                'category_name': categoryName       // add the country id to the GET parameters
            },
            success: function (data) {   // `data` is the return of the `load_cities` view function
                // $("#id_city").html(data);  // replace the contents of the city input with the data that came from the server
              
                document.getElementById("hidden").value = categoryName;
                document.getElementById("hidden1").value = categoryName;

                let html_data = '<option value="">انتخاب...</option>';
                data.forEach(function (brand) {
                    html_data += `<option value="${brand.id}">${brand.name}</option>`
            
                });
                console.log(html_data);
                $("#SelectBrandCategory").html(html_data);
                $("#SelectBrandCategoryDelete").html(html_data);
                


            }
        });

    });


    const formd= document.getElementById('formAdd');
    // const url = $("#formAdd").attr("data-brands");
    formd.addEventListener('submit',submitHandle);
    function submitHandle(e){
                e.preventDefault();
    $.ajax(
        {
            type:'POST',
            url:url,
            data:$('#formAdd').serialize(),
            dataType:'json',
            cache: false,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            success:function (data){
                if (data.msg == 'success'){ 
                    alert('با موفقیت ثبت شد')
                    formd.reset() 
                } else if (data.msg == 'exists'){ 
                    alert('این دسته از قبل وارد شده است')
                    
                }
            },
            error:function (data){
                if (data.msg == 'error'){
                    alert('error')
                }
            }
        }
    )
    }



    const formed = document.getElementById('formedit');
    
    formed.addEventListener('submit',submitHandle);
    function submitHandle(e){
                e.preventDefault();
    $.ajax(
        {
            type:'POST',
            // url:"{% url 'edit-brand-category'%}",
            data:$('#formedit').serialize(),
            dataType:'json',
            cache: false,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            success:function (data){
                if (data.msg == 'success'){
                    
                    alert('ویرایش انحام شد')
                    formed.reset() 
                } else if (data.msg == 'exists'){ 
                    alert('این دسته از قبل وارد شده است')
                    
                }
            },
            error:function (data){
                if (data.msg == 'error'){
                    alert('error')
                }(jQuery)
            }
        }
    )
    }



    const formde= document.getElementById('formDelete');
    formde.addEventListener('submit',submitHandle);
    function submitHandle(e){
                e.preventDefault();
    $.ajax(
        {
            type:'POST',
            // url:"{% url 'edit-brand-category'%}",
            data:$('#formDelete').serialize(),
            dataType:'json',
            cache: false,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            success:function (data){
                if (data.msg == 'success'){
                    
                    alert('عملیات حذف با موفقیت انجام شد')
                    formde.reset() 
                }if (data.msg == 'protectederror'){
                    
                    alert('برای حذف این مورد ابتدا باید تمام دستگاه هایی که به آن ارجاع داده شده اند را حذف کنید.')
                    formde.reset() 
                }
            },
            error:function (data){
                if (data.msg == 'error'){
                    alert('error')
                }(jQuery)
            }
        }
    )
    }
