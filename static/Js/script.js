const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menuToggle');
const closeSidebar = document.getElementById('closeSidebar');

menuToggle.addEventListener('click', () => {
    sidebar.classList.add('active');
});

closeSidebar.addEventListener('click', () => {
    sidebar.classList.remove('active');
});

// Close sidebar when clicking outside
document.addEventListener('click', (event) => {
    if (!sidebar.contains(event.target) && event.target !== menuToggle) {
        sidebar.classList.remove('active');
    }
});

// Close sidebar when a link is clicked
const sidebarLinks = document.querySelectorAll('.sidebar-links a');
sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
        sidebar.classList.remove('active');
    });
});
// Check if the user is logged in (you need to implement this logic)
const isLoggedIn = checkUserLoginStatus(); // Replace with your actual login check logic

// Get the profile icon element
const profileIcon = document.getElementById('profile-icon');

// Show the profile icon if the user is logged in
if (isLoggedIn) {
    profileIcon.style.display = 'block';
}