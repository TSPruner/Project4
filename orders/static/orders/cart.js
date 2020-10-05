document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    var alink = document.querySelector('#login');
    alink.href = "";
    document.getElementById('review-all').style.display = 'none';

    // Set links up to scroll to parts of the current page.
    document.querySelectorAll('.nav-link').forEach(link => {
        link.onclick = () => {
            var el = link;
            if (el.dataset.page == "ShowReviews") {
                el.innerHTML = 'Hide Reviews';      
                el.dataset.page = "HideReviews"
                document.getElementById('review-all').style.display = 'block';
            }
            else {
                el.innerHTML = 'View Reviews';      
                el.dataset.page = "ShowReviews";
                document.getElementById('review-all').style.display = 'none'; 
            }
            return false;
        };
    });
});

