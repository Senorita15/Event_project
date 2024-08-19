
$("#table1").DataTable({
    paging:true,
    pageLength:10,
    lengthChange:true,
    autoWidth:true,
    searching:true,
    bInfo:true,
    bSort:true
})

$("#table2").DataTable({
    paging:true,
    pageLength:10,
    lengthChange:true,
    autoWidth:true,
    searching:true,
    bInfo:true,
    bSort:true
})
// $("#table20").DataTable({
//     paging:true,
//     pageLength:10,
//     lengthChange:true,
//     autoWidth:true,
//     searching:true,
//     bInfo:true,
//     bSort:true
// })
function initialiser() {
    // Code pour réinitialiser les champs du formulaire ou effectuer d'autres actions
    alert("Bouton Initialiser cliqué !");
}

// $(function(){
//     $('#formation_id').on("change",function(){

//         formation_id=$(this).val();
//         alert(formation_id);
//         $.get(
//             "/admin/evaluations/getcours",

//             {
//                 formation_id:formation_id
//             },
//             function(data,textStatus,jqXHR)
//             {
//                 $("#id_cours").html(data);
//             }
//         );
//     });
// });


// $(function(){
//     $('#formation').on("change",function(){

//         formation=$(this).val();
//         alert(formation);
//         $.get(
//             "/admin/formateurs/templates/presence_acteurs/getcourse",
//             {
//                 formation:formation
//             },
//             function(data,textStatus,jqXHR)
//             {
//                 $("#id_cours").html(data);
//             }
//         );
//     });
// });
