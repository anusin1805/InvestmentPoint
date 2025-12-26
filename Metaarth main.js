var mnav = 0, hiddensiteurl = "";
var hrefurl = window.location.href, hrefvar;
$(document).ready(function () {
    hiddensiteurl = $('#hdndomainname').val();
    pagename = $('#hdnpagename').val();
    $('a[href="#"]').click(function (e) { e.preventDefault(); });
    $('.matchHeight').matchHeight();
    $('[data-toggle="tooltip"]').tooltip();

    $("#mobnav").click(function () {
        if (mnav === 0) {
            $(this).addClass("Nclose");
            $(".slidenav").addClass("open");
            mnav = 1;
        } else {
            $(this).removeClass("Nclose");
            $(".slidenav").removeClass("open");
            mnav = 0;
        }
    });
    $("#nclose").click(function () {
        $("#mobnav").removeClass("Nclose");
        $(".slidenav").removeClass("open");
        mnav = 0;
    });
    $(".wealthpickrdmore").click(function () {
        var info = $(this).attr('data-info');
        $('.wealthpickdata').hide();
        $('#' + info).show();
        $('#wealthpickpopup').modal('show');
    });
    $(".fullmenubg").clone().insertAfter("#nclose");

    $('.scrollup').hide();
    $(window).scroll(function () {
        if ($(this).scrollTop() > 500) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });
    $('.scrollup').click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });
    $(window).scroll(fixDiv, fixGetinTouch);
    fixDiv();
    //$(window).scroll(fixGetinTouch);
    fixGetinTouch();
    if ($("#mfloginedinfo").length > 0) {
        if ($("#mfloginedinfo").val() == "true") {
            $("body").addClass("logined");
            $("a.login").html("DashBoard").attr("href", hiddensiteurl + "/pages/mydashboard.aspx").attr("title", "Dashboard");
        }
    }

    // header selection
    hrefvar = hrefurl.split('?')[0].split('/');
    hrefvar = hrefvar.slice(-1)[0];
    var linktagheader = $('#mnav li a[href*="/' + hrefvar + '"]');

    if (pagename != "default") {
        $(linktagheader).closest('li').addClass('active');

    }

    if (pagename == "default") {

        $("ul.HmeMktMenu > li").click(function () {
            $("ul.HmeMktMenu > li").removeClass("active");
            $(this).addClass("active");
            GetPerformance($(this).attr('data-cat-value'));
        });

        GetPerformance("31,49");
        /*testimonial slide*/
        $("#customersayslider").find('.owl-carousel').owlCarousel({
            margin: 20,
            loop: false,
            nav: false,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1
                },
                767: {
                    items: 2
                },
                991: {
                    items: 2
                },
                1200: {
                    items: 2
                }
            }
        });

        $("#homegoal").find('.owl-carousel').owlCarousel({
            margin: 20,
            loop: false,
            nav: true,
            navText: [
        "<i class='fa fa-chevron-left'></i>",
        "<i class='fa fa-chevron-right'></i>"
        ],
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1
                },
                767: {
                    items: 3
                },
                991: {
                    items: 5
                },
                1200: {
                    items: 5
                }
            }
        });
    }

});


function fixDiv() {
    var $cache = $('body');
    if ($("#hdnpagename").val() == "default") {
        if ($(window).scrollTop() > 220) {
            $cache.addClass("fix");
        } else {
            $cache.removeClass("fix");
        }
    }
    else {
        $cache.addClass("fix");
    }
}
function fixGetinTouch() {
    var $cachenew = $('#footerB');
    if ($(window).scrollTop() > 220) {
        $cachenew.addClass("fix");
    }
    else {
        $cachenew.removeClass("fix");
    }
}
function RedirectAndPOST(url, jsondata, target) {
    if (target == undefined) {
        target = "_self";
    }
    var form = "<form action=\"" + url + "\" method=\"post\" target=\"" + target + "\">";
    if (jsondata != undefined && jsondata != null && jsondata != "") {
        $.each(jsondata, function (key, value) {
            form += ("<input type=\"hidden\" name=\"" + key + "\" value=\"" + value + "\" />");
        });
    }
    form += ("</form>");

    form = $(form);
    $('body').append(form);
    form.submit();
}

function GetPerformance(Category) {
    $("#mftopdata").html("<div class=\"ajaxloaderhmediv\"></div>");
    var tempUrl = hiddensiteurl + "/default.aspx/mfperformance";
    var obj = {};
    obj.Category = Category;
    $.ajax({
        type: "POST",
        url: tempUrl,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(obj),
        dataType: "json",
        success: function (response) {
            $("#mftopdata").html(response.d[0]);
        },
        error: function (x, e) {
        }
    });
}

function GetinTouchValidation(name,email,mob) {
    var email = document.getElementById(email);
    var phone = document.getElementById(mob);
    var fname = document.getElementById(name);

    if (fname.value == "") {
        alertify.alert("Please Enter Name", function () { setTimeout(function () {fname.focus(); },300) });        
        return false;
    }
    else if (phone.value == "") {
        alertify.alert("Please Enter Mobile Number", function () { setTimeout(function () { phone.focus(); }, 300) });        
        return false;
    }
    else if (email.value == "") {
        alertify.alert("Please Enter Email Id", function () { setTimeout(function () { email.focus(); }, 300) });        
        return false;
    }
    else { SaveGetinTouch(fname, phone, email); }
}

function SaveGetinTouch(name, phone, email) {
    $.ajax({
        type: "POST",
        url: hiddensiteurl + "/Ajaxpages/common_ajax.aspx/GetinTouch",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ name: name.value, email: email.value, mobile: phone.value }),
        success: function (res) {
            if (res.d == "success") {
                ClearGetinTouch(name, phone, email);
                $("#getintouchpop").modal('hide');
                alertify.alert("Thank you for shairing your details. We will contact you soon!")
            }

        }

    });
}
function ClearGetinTouch(name, phone, email) {
    email.value = '';
    phone.value = '';
    name.value = '';
}

function phonenovalidate(tboxid) {
    var userinput = $("#" + tboxid).val();
    if (userinput != "") {
        var filter = /^[6-9]\d{9}$/;
        if (filter.test(userinput)) {
            $("#" + tboxid).attr('data-original-title', '');
            return true;
        }
        else {
            $("#" + tboxid).attr('data-original-title', 'Invalid Mobile Number! Please Re enter..');
            $("#" + tboxid).tooltip('show');
            $("#" + tboxid).val('');
            $("#" + tboxid).focus();
            $("#" + tboxid).addClass('blured');
            return false;
        }
    }
}
function emailvalidate(tboxid) {
    var userinput = $("#" + tboxid).val();
    if (userinput != "") {
        var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
        if (filter.test(userinput)) {
            $("#" + tboxid).attr("data-original-title", "");
            return true;
        }
        else {
            $("#" + tboxid).attr("data-original-title", "'" + userinput + "' Invalid E-mail Address! Please re-enter.");
            $("#" + tboxid).tooltip('show');
            $("#" + tboxid).val('');
            $("#" + tboxid).focus();
            $("#" + tboxid).addClass('blured');
            return false;
        }
    }
}
function showgetintouchpop(newsId) {
    $("#getintouchpop").modal('show');
}
