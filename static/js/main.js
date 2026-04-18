$(document).ready(function () {

    // ─── SERVICES PAGE: Load services via AJAX ────────────────
    if ($('#ajax-services-container').length) {

        // Show loading state
        $('#ajax-services-container').html(
            '<p style="text-align:center;color:#666;padding:30px;">Loading services...</p>'
        );

        $.ajax({
            url: '/api/services/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log('Services JSON received:', data);

                // Build service cards from JSON response
                var html = '';
                $.each(data, function (index, service) {
                    html += '<div class="service-card" id="service-' + service.id + '">';
                    html += '  <div class="service-header">';
                    html += '    <h3>' + service.name + '</h3>';
                    html += '  </div>';
                    html += '  <div class="service-description">' + service.description + '</div>';
                    html += '  <div class="service-price">Rs ' + service.price + '</div>';
                    html += '  <button type="button" class="book-now-btn ajax-book-btn"';
                    html += '    data-service-id="' + service.id + '"';
                    html += '    data-service-name="' + service.name + '">';
                    html += '    Book Now';
                    html += '  </button>';
                    html += '  <div class="ajax-booking-response" id="response-' + service.id + '" style="display:none;margin-top:10px;"></div>';
                    html += '</div>';
                });

                $('#ajax-services-container').html(html);
                $('#ajax-status').html(
                    '<p style="color:#28a745;font-size:13px;text-align:center;">' +
                    '✓ ' + data.length + ' services loaded via AJAX from /api/services/</p>'
                );
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error);
                $('#ajax-services-container').html(
                    '<p style="color:red;text-align:center;">Failed to load services.</p>'
                );
            }
        });

        // ── Book Now button click via AJAX ─────────────────────
        $(document).on('click', '.ajax-book-btn', function () {
            var serviceId = $(this).data('service-id');
            var serviceName = $(this).data('service-name');
            var responseDiv = $('#response-' + serviceId);

            // Redirect to booking page with service pre-selected
            window.location.href = '/bookings/create/?service_id=' + serviceId;
        });
    }


    // ─── CONTACT PAGE: Load branches via AJAX ─────────────────
    if ($('#ajax-branches-container').length) {

        $('#ajax-branches-container').html(
            '<p style="text-align:center;color:#666;padding:20px;">Loading branch locations...</p>'
        );

        $.ajax({
            url: '/api/branches/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log('Branches JSON received:', data);

                var html = '';
                $.each(data, function (index, branch) {
                    html += '<div class="contact-background-border">';
                    html += '  <div class="contact-div-wrapper-2"><div class="contact-text-wrapper-5">' + branch.name + '</div></div>';
                    html += '  <div class="contact-div-wrapper-2"><div class="contact-text-wrapper-6">' + branch.address + '</div></div>';
                    html += '  <div class="contact-div-wrapper-2"><div class="contact-text-wrapper-7">Tel: ' + branch.phone + '</div></div>';
                    html += '  <div class="contact-div-wrapper-2"><div class="contact-text-wrapper-7">Hours: ' + branch.hours + '</div></div>';
                    html += '</div>';
                });

                $('#ajax-branches-container').html(html);
                $('#ajax-branches-status').html(
                    '<p style="color:#28a745;font-size:13px;text-align:center;">' +
                    '✓ ' + data.length + ' branches loaded via AJAX from /api/branches/</p>'
                );
            },
            error: function (xhr, status, error) {
                console.error('Branches AJAX error:', error);
                $('#ajax-branches-container').html(
                    '<p style="color:red;">Failed to load branch locations.</p>'
                );
            }
        });
    }

});