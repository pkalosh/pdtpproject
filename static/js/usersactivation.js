<script>
$('.like').click(function(){
      $.ajax({
               type: "POST",
               url: "{% url 'deactivate' %}",
               data: {'id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
               dataType: "json",
               success: function(response) {
                      notify('success', response.message);
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          }); 
    })
</script>

<script>
$('.activate').click(function(){
      $.ajax({
               type: "POST",
               url: "{% url 'activate' %}",
               data: {'id': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
               dataType: "json",
               success: function(response) {
                      notify('success', response.message);
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          }); 
    })
</script>
