// document.querySelector(".jsFilter").addEventListener("click", function () {
//     document.querySelector(".filter-menu").classList.toggle("active");
//   });
  
//   document.querySelector(".grid").addEventListener("click", function () {
//     document.querySelector(".list").classList.remove("active");
//     document.querySelector(".grid").classList.add("active");
//     document.querySelector(".products-area-wrapper").classList.add("gridView");
//     document
//       .querySelector(".products-area-wrapper")
//       .classList.remove("tableView");
//   });
  
//   document.querySelector(".list").addEventListener("click", function () {
//     document.querySelector(".list").classList.add("active");
//     document.querySelector(".grid").classList.remove("active");
//     document.querySelector(".products-area-wrapper").classList.remove("gridView");
//     document.querySelector(".products-area-wrapper").classList.add("tableView");
//   });
  
//   var modeSwitch = document.querySelector('.mode-switch');
//   modeSwitch.addEventListener('click', function () {
//     document.documentElement.classList.toggle('light');
//     modeSwitch.classList.toggle('active');
//   });
document.addEventListener("DOMContentLoaded", function () {
  const sidebarItems = document.querySelectorAll(".sidebar-list-item");

  // Find the "Home" sidebar item and trigger a click event on it
  const homeSidebarItem = document.querySelector(".sidebar-list-item[data-page='accounts/home'] a");
  homeSidebarItem.click();

  sidebarItems.forEach(function (item) {
    item.addEventListener("click", function () {
      // Remove 'active' class from all navigation items
      sidebarItems.forEach(function (otherItem) {
        otherItem.classList.remove("active");
      });

      // Add 'active' class to the clicked navigation item
      this.classList.add("active");
    });
  });
});

$(document).ready(function() {
  setActiveItem('accounts/home');
  $('.sidebar-list-item').on('click', function(e) {
      e.preventDefault();
      var page = $(this).attr('data-page');
      loadPage(page);
  });
});
function setActiveItem(page) {
  loadPage("accounts/home");
}

function loadPage(page) {
  $.ajax({
      url: '/' + page + '/',
      type: 'GET',
      success: function(data) {
          $('#content').html(data);
      },
      error: function(xhr, status, error) {
          console.error(error);
      }
  });
}


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Check if the cookie contains the specified name
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


  
  
  // // Function to toggle the visibility of the products container
  // function toggleProducts() {
  //   var productsContainer = document.getElementById("productsContainer");
  //   var facultyContainer = document.getElementById("facultyContainer");
  //   var coursesContainer = document.getElementById("coursesContainer");
  //   var topicsContainer = document.getElementById("topicsContainer");
  
  //   facultyContainer.classList.add("hidden");
  //   coursesContainer.classList.add("hidden");
  //   topicsContainer.classList.add("hidden");
  //   productsContainer.classList.remove("hidden");
  // }
  
  // // Function to toggle the visibility of the faculty container
  // function toggleFaculty() {
  //   var productsContainer = document.getElementById("productsContainer");
  //   var facultyContainer = document.getElementById("facultyContainer");
  //   var coursesContainer = document.getElementById("coursesContainer");
  //   var topicsContainer = document.getElementById("topicsContainer");
  
  //   productsContainer.classList.add("hidden");
  //   coursesContainer.classList.add("hidden");
  //   topicsContainer.classList.add("hidden");
  //   facultyContainer.classList.remove("hidden");
  // }
  
  // // Function to toggle the visibility of the courses container
  // function toggleCourses() {
  //   var productsContainer = document.getElementById("productsContainer");
  //   var facultyContainer = document.getElementById("facultyContainer");
  //   var coursesContainer = document.getElementById("coursesContainer");
  //   var topicsContainer = document.getElementById("topicsContainer");
  
  //   productsContainer.classList.add("hidden");
  //   facultyContainer.classList.add("hidden");
  //   topicsContainer.classList.add("hidden");
  //   coursesContainer.classList.remove("hidden");
  // }
  
  // // Function to toggle the visibility of the topics container
  // function toggleTopics() {
  //   var productsContainer = document.getElementById("productsContainer");
  //   var facultyContainer = document.getElementById("facultyContainer");
  //   var coursesContainer = document.getElementById("coursesContainer");
  //   var topicsContainer = document.getElementById("topicsContainer");
  
  //   productsContainer.classList.add("hidden");
  //   facultyContainer.classList.add("hidden");
  //   coursesContainer.classList.add("hidden");
  //   topicsContainer.classList.remove("hidden");
  // }
  
  // document.addEventListener("DOMContentLoaded", function () {
  //   const sidebarItems = document.querySelectorAll(".sidebar-list-item");
  
  //   sidebarItems.forEach(function (item) {
  //     item.addEventListener("click", function () {
  //       // Remove 'active' class from all navigation items
  //       sidebarItems.forEach(function (otherItem) {
  //         otherItem.classList.remove("active");
  //       });
  
  //       // Add 'active' class to the clicked navigation item
  //       this.classList.add("active");
  //     });
  //   });
  
  //   // Add event listeners for other functionalities here
  // });
  