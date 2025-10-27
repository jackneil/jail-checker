
// Helper function to handle broken images
function handleBrokenImages() {
    var fallbackSrc = 'https://analytics.southernsoftware.com/crons/CCMugshots/NoMugshot.jpg';
    
    setTimeout(function() {
        $('img').each(function() {
            if (this.src && this.src.includes('Mugshot') && this.src !== fallbackSrc) {
                // Check if already broken
                if (this.complete && this.naturalWidth === 0) {
                    this.src = fallbackSrc;
                }
                // Add error handler
                this.onerror = function() {
                    if (this.src !== fallbackSrc) {
                        this.src = fallbackSrc;
                    }
                };
            }
        });
    }, 100);
}

// Global handlers for any mugshot images
$(document).on('error', 'img.booking-mugshot', function() {
    var fallbackSrc = 'https://analytics.southernsoftware.com/crons/CCMugshots/NoMugshot.jpg';
    if (this.src !== fallbackSrc) {
        this.src = fallbackSrc;
    }
});

$(document).on('error', 'img', function() {
    if (this.src && this.src.includes('Mugshot')) {
        var fallbackSrc = 'https://analytics.southernsoftware.com/crons/CCMugshots/NoMugshot.jpg';
        if (this.src !== fallbackSrc) {
            this.src = fallbackSrc;
        }
    }
});

// Helper function to clear all search results
function clearAllSearchResults() {
    $('#invlist').empty().hide();
    $('#listcharge').empty().hide();
    $('#listarrestagency').empty().hide();
    $('#listchargeagency').empty().hide();
    $('#listname').empty().hide();
    $('#currentconfinementsall').empty().hide();
    $('#last24admits').empty().hide();
    
    // Hide all date range divs
    for(var i = 1; i <= 27; i++) {
        if(i === 10) continue; // Skip 10 as it doesn't exist in the pattern
        $('#listdaterange' + (i === 1 ? '' : i)).empty().hide();
    }
}

$(function() {
    $("#formdaterangeadmit").on('submit', function (e) {
        e.preventDefault();
        var tmpdatediff = null

        // Debug: Log form data
        var formData = $('#formdaterangeadmit').serialize();
        console.log('=== ADMITS DATE RANGE DEBUG ===');
        console.log('Form data being sent:', formData);
        console.log('Begin date:', $('#begindate').val());
        console.log('End date:', $('#enddate').val());
        console.log('Radio selection:', $('input[name="customRadioInline1"]:checked').val());

        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_datediff.php',
            data: formData,
            beforeSend: function () {
                clearAllSearchResults();
                $('#listname').show();
            },
            success: function (html) {
                tmpdatediff = html;
                console.log('Date difference calculated:', tmpdatediff);

                if (tmpdatediff < 365) {  // Allow up to 1 year date range
                    console.log('Date range is valid, fetching admits...');
                    $.ajax({
                        type: 'POST',
                        url: 'fetchesforajax/fetch_incident_search_dates_admit.php',
                        data: $('#formdaterangeadmit').serialize(),
                        beforeSend: function(){
                            $("#IncidentGridloader").show();
                        },
                        success: function (html) {
                            console.log('Admits response received, length:', html.length);
                            console.log('First 500 chars of response:', html.substring(0, 500));
                            $('#listname').html(html);
                            // Handle broken images after content is loaded
                            handleBrokenImages();

                        },
                        error: function(xhr, status, error) {
                            console.error('Error fetching admits:', error);
                            console.error('XHR status:', xhr.status);
                            console.error('Response text:', xhr.responseText);
                        },
                        complete: function(){
                            $("#IncidentGridloader").hide();
                        },
                    })
                } else {
                    $.ajax({

                        success: function (html) {
                            $('#datedifferror').show();
                        }
                    })
                }
            }
        })
    });
});

$(function() {
    $("#formdaterangerelease").on('submit', function (e) {
        e.preventDefault();
        var tmpdatediff = null
        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_datediff.php',
            data: $('#formdaterangerelease').serialize(),
            beforeSend: function () {
                clearAllSearchResults();
                $('#listname').show();
            },
            success: function (html) {
                console.log('function 1 success');
                tmpdatediff = html;
                if (tmpdatediff < 365) {  // Allow up to 1 year date range
                    $.ajax({
                        type: 'POST',
                        url: 'fetchesforajax/fetch_incident_search_dates_release.php',
                        data: $('#formdaterangerelease').serialize(),
                        beforeSend: function(){
                            $("#IncidentGridloader").show();
                        },
                        success: function (html) {
                            console.log('function 2 success');
                            $('#listname').html(html);
                            // Handle broken images after content is loaded
                            handleBrokenImages();

                        },
                        complete: function(){
                            $("#IncidentGridloader").hide();
                        },
                    })
                } else {
                    $.ajax({

                        success: function (html) {
                            $('#datedifferror').show();
                        }
                    })
                }
            }
        })
    });
});

$(function() {
    $("#formname").on('submit', function (e) {
        e.preventDefault();
        $('#listname').show();
        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_incident_search_name.php',
            data: $('#formname').serialize(),
            beforeSend: function(){
                $("#IncidentGridloader").show();
                clearAllSearchResults();
            },
            success: function (html) {
                console.log(html);
                $('#listname').html(html).show();
                // Handle broken images after content is loaded
                handleBrokenImages();
            },
            complete:function(){
                $("#IncidentGridloader").hide();
            }
        })
    });
});

$(function() {
    $("#formcharge").on('submit', function (e) {
        e.preventDefault();
        $('#listcharge').show();
        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_incident_search_charge.php',
            data: $('#formcharge').serialize(),
            beforeSend: function(){
                $("#IncidentGridloader").show();
                clearAllSearchResults();
            },
            success: function (html) {
                /*console.log(html);*/
                $('#listcharge').html(html).show();
                // Handle broken images after content is loaded
                handleBrokenImages();
            },
            complete:function(){
                $("#IncidentGridloader").hide();
            }
        })
    });
});

$(function() {
    $("#formarrestagency").on('submit', function (e) {
        e.preventDefault();
        $('#listarrestagency').show();
        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_incident_search_arrestagency.php',
            data: $('#formarrestagency').serialize(),
            beforeSend: function(){
                $("#IncidentGridloader").show();
                clearAllSearchResults();
            },
            success: function (html) {
                /*console.log(html);*/
                $('#listarrestagency').html(html).show();
                // Handle broken images after content is loaded
                handleBrokenImages();
            },
            complete:function(){
                $("#IncidentGridloader").hide();
            }
        })
    });
});

$(function() {
    $("#formchargeagency").on('submit', function (e) {
        e.preventDefault();
        $('#listchargeagency').show();
        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_incident_search_chargeagency.php',
            data: $('#formchargeagency').serialize(),
            beforeSend: function(){
                $("#IncidentGridloader").show();
                clearAllSearchResults();
            },
            success: function (html) {
                /*console.log(html);*/
                $('#listchargeagency').html(html).show();
                // Handle broken images after content is loaded
                handleBrokenImages();
            },
            complete:function(){
                $("#IncidentGridloader").hide();
            }
        })
    });
});

$(function() {
    $("#formgetcurrentconfinements").on('submit', function (e) {

        e.preventDefault();
        $('#currentconfinementsall').show();
      $.ajax({
        type: 'POST',
        url: 'fetchesforajax/fetch_current_confinements.php',
        data: $.extend($('#formcurrentconfinementsonload').serializeObject(), {
            search: '',
            agency: '',
            sort: 'name'
        }),
        beforeSend: function () {
          $("#CurrentConfinementsloader").show();
          clearAllSearchResults();
          $('#currentconfinementsall').show();
        },
        success: function (html) {
          $('#currentconfinementsall').html(html);
          // Handle broken images after content is loaded
          handleBrokenImages();

        },
      });

    });
});

$(function() {
    $("#formgetlast24admits").on('submit', function (e) {

        e.preventDefault();
        $('#last24admits').show();
        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_last24hours.php',
            data: $('#formcurrentconfinementsonload').serialize(),
            beforeSend: function () {
                $("#CurrentConfinementsloader").show();
                clearAllSearchResults();
                $('#last24admits').show();
            },
            success: function (html) {
                $('#last24admits').html(html);
                // Handle broken images after content is loaded
                handleBrokenImages();

            },
        });

    });
});



function submit() {

}








    $(document).ready(function() {
        // Clear all search results on page load
        clearAllSearchResults();
        
        $.ajax({
            type: 'POST',
            url: 'fetchesforajax/fetch_current_confinements.php',
            data: $.extend($('#formcurrentconfinementsonload').serializeObject(), {
                search: '',
                agency: '',
                sort: 'name'
            }),
            beforeSend: function () {
                $("#CurrentConfinementsloader").show();
            },
            success: function (html) {
                $('#currentconfinementsall').html(html).show();
                
                // Handle broken images after content is loaded
                handleBrokenImages();
                
                // Multiple checks to catch all images
                setTimeout(handleBrokenImages, 500);
                setTimeout(handleBrokenImages, 1000);
                setTimeout(handleBrokenImages, 2000);
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', status, error);
                $('#currentconfinementsall').html('<div class="alert alert-danger">Error loading data. Please refresh the page.</div>').show();
            }
        });
        submit();
    });
    
    // Helper function to serialize form to object
    $.fn.serializeObject = function() {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };



        function Nextpage(IDX, search, agency, sort) {
          window.scrollTo(0, 0);
          
          // Get current filter values if not passed as parameters
          var searchTerm = search || $('#searchInput').val() || '';
          var agencyFilter = agency || $('#agencyFilter').val() || '';
          var sortBy = sort || $('#sortBy').val() || 'name';
          
        $.ajax({
            type: "POST",
          url: 'fetchesforajax/fetch_current_confinements.php',

            data: {
                IDX: IDX,
                search: searchTerm,
                agency: agencyFilter,
                sort: sortBy
            },
            success: function(html){
              $('#currentconfinementsall').html(html);
                $('#confinementsubmit').show();
                // Handle broken images after content is loaded
                handleBrokenImages();
            }
        })
    }
    
    // New function to apply filters
    function applyFilters() {
        var searchTerm = $('#searchInput').val();
        var agencyFilter = $('#agencyFilter').val();
        var sortBy = $('#sortBy').val();
        
        Nextpage(1, searchTerm, agencyFilter, sortBy);
    }
    
    // Handle enter key in search input
    $(document).on('keypress', '#searchInput', function(e) {
        if (e.which === 13) {
            e.preventDefault();
            applyFilters();
        }
    });

function Nextpage24(IDX) {
    window.scrollTo(0, 0);
    $.ajax({
        type: "POST",
        url: 'fetchesforajax/fetch_last24hours.php',

        data: {IDX: IDX},
        success: function(html){
            $('#last24admits').html(html);
            $('#confinementsubmit').show();
            // Handle broken images after content is loaded
            handleBrokenImages();
        }
    })
}

// Function for last 24 hours pagination (matches the onclick in the PHP)
function getlast24admits(IDX) {
    window.scrollTo(0, 0);
    $.ajax({
        type: "POST",
        url: 'fetchesforajax/fetch_last24hours.php',
        data: $('#formcurrentconfinementsonload').serialize() + '&IDX=' + IDX,
        beforeSend: function () {
            $("#CurrentConfinementsloader").show();
        },
        success: function(html){
            $('#last24admits').html(html);
            $('#confinementsubmit').show();
            // Handle broken images after content is loaded
            handleBrokenImages();
        },
        complete: function () {
            $("#CurrentConfinementsloader").hide();
        }
    })
}















function mobileMenuNavBar() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}
