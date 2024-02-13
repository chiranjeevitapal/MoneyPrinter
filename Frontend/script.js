$(document).ready(function () {
    // Dynamically add select options on page load
    const voiceSelect = $('#voice');
    const voices = [
            { value: 'en_us_ghostface', text: 'Ghost Face' },
            { value: 'en_us_chewbacca', text: 'Chewbacca' },
            { value: 'en_us_c3po', text: 'C3PO' },
            { value: 'en_us_stitch', text: 'Stitch' },
            { value: 'en_us_stormtrooper', text: 'Stormtrooper' },
            { value: 'en_us_rocket', text: 'Rocket' },
            { value: 'en_au_001', text: 'English AU - Female' },
            { value: 'en_au_002', text: 'English AU - Male' },
            { value: 'en_uk_001', text: 'English UK - Male 1' },
            { value: 'en_uk_003', text: 'English UK - Male 2' },
            { value: 'en_us_001', text: 'English US - Female (Int. 1)' },
            { value: 'en_us_002', text: 'English US - Female (Int. 2)' },
            { value: 'en_us_006', text: 'English US - Male 1' },
            { value: 'en_us_007', text: 'English US - Male 2' },
            { value: 'en_us_009', text: 'English US - Male 3' },
            { value: 'en_us_010', text: 'English US - Male 4' },
            { value: 'fr_001', text: 'French - Male 1' },
            { value: 'fr_002', text: 'French - Male 2' },
            { value: 'de_001', text: 'German - Female' },
            { value: 'de_002', text: 'German - Male' },
            { value: 'es_002', text: 'Spanish - Male' },
            { value: 'es_mx_002', text: 'Spanish MX - Male' },
            { value: 'br_001', text: 'Portuguese BR - Female 1' },
            { value: 'br_003', text: 'Portuguese BR - Female 2' },
            { value: 'br_004', text: 'Portuguese BR - Female 3' },
            { value: 'br_005', text: 'Portuguese BR - Male' },
            { value: 'id_001', text: 'Indonesian - Female' },
            { value: 'jp_001', text: 'Japanese - Female 1' },
            { value: 'jp_003', text: 'Japanese - Female 2' },
            { value: 'jp_005', text: 'Japanese - Female 3' },
            { value: 'jp_006', text: 'Japanese - Male' },
            { value: 'kr_002', text: 'Korean - Male 1' },
            { value: 'kr_003', text: 'Korean - Female' },
            { value: 'kr_004', text: 'Korean - Male 2' },
            { value: 'en_female_f08_salut_damour', text: 'Alto' },
            { value: 'en_male_m03_lobby', text: 'Tenor' },
            { value: 'en_female_f08_warmy_breeze', text: 'Warmy Breeze' },
            { value: 'en_male_m03_sunshine_soon', text: 'Sunshine Soon' },
            { value: 'en_male_narration', text: 'narrator' },
            { value: 'en_male_funny', text: 'wacky' },
            { value: 'en_female_emotional', text: 'peaceful' }
        ];

    voices.forEach(voice => {
        voiceSelect.append(`<option value="${voice.value}">${voice.text}</option>`);
    });

    // Generate video function
    $('#generateButton').click(function () {
        console.log("Generating video...");
        $('#generateButton').prop('disabled', true).addClass('hidden');
        $('#cancelButton').removeClass('hidden');
        const videoSubjectValue = $('#videoSubject').val();
        const voiceValue = $('#voice').val();
        const youtubeUpload = $('#youtubeUploadToggle').prop('checked');
        const maxVideoDuration = $('#maxVideoDuration').val();
        const url = "http://localhost:8080/api/generate";
        const data = {
            videoSubject: videoSubjectValue,
            voice: voiceValue,
            maxVideoDuration: maxVideoDuration,
            automateYoutubeUpload: youtubeUpload,
        };
        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                console.log(response);
                alert(response.message);
                $('#generateButton').prop('disabled', false).removeClass('hidden');
                $('#cancelButton').addClass('hidden');
            },
            error: function (error) {
                alert("An error occurred. Please try again later.");
                console.log(error);
            }
        });
    });

    // Cancel generation function
    $('#cancelButton').click(function () {
        console.log("Canceling generation...");
        $.ajax({
            type: "POST",
            url: "http://localhost:8080/api/cancel",
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                alert(response.message);
                console.log(response);
            },
            error: function (error) {
                alert("An error occurred. Please try again later.");
                console.log(error);
            }
        });
        $('#cancelButton').addClass('hidden');
        $('#generateButton').prop('disabled', false).removeClass('hidden');
    });

    // Trigger generation on Enter key press
    $('#videoSubject').keyup(function (event) {
        if (event.key === "Enter") {
            $('#generateButton').click();
        }
    });

    // Load stored voice value from localStorage on page load
    const storedVoiceValue = localStorage.getItem('voiceValue');
    if (storedVoiceValue) {
        $('#voice').val(storedVoiceValue);
    }

    // Store selected voice value in localStorage
    $('#voice').change(function (event) {
        localStorage.setItem('voiceValue', $(this).val());
    });
});
