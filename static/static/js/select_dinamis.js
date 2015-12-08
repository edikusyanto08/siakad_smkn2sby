<script>
    $(document).ready(
                     function() {
                         $("select#brand").change(function() {
                             if ($(this).val() == 'Z') {
                                 $("select#model").html("<option>Select a model</option>");
                                 $("select#model").attr('disabled', true);
                             }
                             else {
                                 var url = "/brand/" + $(this).val() + "/all_json_models";
                                 var brand = $(this).val();
                                 $.getJSON(url, function(models) {
                                     var options = '<option value="Z">Select a model</option>';
                                     for (var i = 0; i < models.length; i++) {
                                        options += '<option value="' + models[i].pk + '">' + models[i].fields['description'] + '</option>';
                                     }
                                     $("select#model").html(options);
                                     $("select#model option:first").attr('selected', 'selected');
                                     $("select#model").attr('disabled', false);
                                 });
                             }
                         });


                         $("select#model").change(function(vent) {
                             if ($(this).val() == -1) {
                                 return;
                             }
                             myAwesomeFunctionToCallWhenAModelIsSelected();
                         });
                     });
    }

</script>