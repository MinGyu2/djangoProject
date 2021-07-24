$(document).ready(function () {
    $("#click_menu_1").click(function() {
        $("#click_menu_1").attr('class','menu_container_selected');
        $("#click_menu_2").attr('class','menu_container');
        $("#click_menu_3").attr('class','menu_container');
        $("#click_menu_4").attr('class','menu_container');
        $("#title_select_menu").html('<a>설비 조회</a>')
    });
    $("#click_menu_2").click(function() {
        $("#click_menu_1").attr('class','menu_container');
        $("#click_menu_2").attr('class','menu_container_selected');
        $("#click_menu_3").attr('class','menu_container');
        $("#click_menu_4").attr('class','menu_container');
        $("#title_select_menu").html('<a>관리자 위치</a>')
    });
    $("#click_menu_3").click(function() {
        $("#click_menu_1").attr('class','menu_container');
        $("#click_menu_2").attr('class','menu_container');
        $("#click_menu_3").attr('class','menu_container_selected');
        $("#click_menu_4").attr('class','menu_container');
        $("#title_select_menu").html('<a>에러 로그</a>')
    });
    $("#click_menu_4").click(function() {
        $("#click_menu_1").attr('class','menu_container');
        $("#click_menu_2").attr('class','menu_container');
        $("#click_menu_3").attr('class','menu_container');
        $("#click_menu_4").attr('class','menu_container_selected');
        $("#title_select_menu").html('<a>직원 DB</a>')
    });
})