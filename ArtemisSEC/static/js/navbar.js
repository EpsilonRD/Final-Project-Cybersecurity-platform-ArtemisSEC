document.addEventListener('DOMContentLoaded', function () {
    // Dropdown for user 
    const userDropdown = document.getElementById('userDropdown');
    const userDropdownMenu = document.getElementById('dropdownMenu');

    if (userDropdown && userDropdownMenu) {
        userDropdown.addEventListener('click', function (e) {
            e.preventDefault();
            userDropdownMenu.style.display = userDropdownMenu.style.display === 'block' ? 'none' : 'block';
        });

        // close whe click out 
        document.addEventListener('click', function (e) {
            if (!userDropdown.contains(e.target) && !userDropdownMenu.contains(e.target)) {
                userDropdownMenu.style.display = 'none';
            }
        });
    }

    // Dropdown de Scan Now
    const scanDropdown = document.getElementById('scanDropdown');
    const scanDropdownMenu = document.getElementById('scanDropdownMenu');

    if (scanDropdown && scanDropdownMenu) {
        scanDropdown.addEventListener('click', function (e) {
            e.preventDefault();
            scanDropdownMenu.style.display = scanDropdownMenu.style.display === 'block' ? 'none' : 'block';
        });

        // close when click out 
        document.addEventListener('click', function (e) {
            if (!scanDropdown.contains(e.target) && !scanDropdownMenu.contains(e.target)) {
                scanDropdownMenu.style.display = 'none';
            }
        });
    }
});