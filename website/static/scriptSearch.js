let category = window.location.pathname;
var categories = category.split('/');
category = categories[1];

// Load lại trang
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}


// Bất đồng bộ
document.addEventListener("DOMContentLoaded", async(e) =>  {
    document.getElementById('loading-overlay').style.display = 'flex';
    var name = document.querySelector('.name-key').textContent;
    var count = document.querySelector('.count');
    var nothing = document.querySelector('.nothing');

    window.history.pushState('', '', "/search?name=" + String(name) + "&page=1&sort=1");
    let response = await fetch(`/searchProduct?name=${name}&page=1&sort=1`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(name),
    }).then((res) => res.json());
    count.innerHTML = `Tìm thấy ${response["total"]} sản phẩm.`;
    document.querySelector(".sort-select").innerHTML = response["sort"];
    if (response["total"] !== 0)
    {
        document.querySelector(".listproduct").innerHTML = response["listproduct"];
        document.querySelector(".pagination").innerHTML = response["pagination"];
    }
    else nothing.classList.remove("hidden");
    document.getElementById('loading-overlay').style.display = 'none';
    sortProduct();
    movePagination();
});


// Sắp xếp sản phẩm
sortProduct();
function sortProduct() {

    document.querySelectorAll("#sortButton").forEach((sortButton) => {
        sortButton.addEventListener("click", async(e) => {
            let sortType = sortButton.getAttribute('value');
            var name = document.querySelector('.name-key').textContent;
            var nothing = document.querySelector('.nothing');

            e.stopPropagation();
            e.stopImmediatePropagation();
            e.preventDefault();

            window.history.pushState('newSort', '', "/search?name=" + String(name) + "&page=1&sort=" + String(sortType));
            document.getElementById('loading-overlay').style.display = 'flex';
            let response = await fetch(`/searchProduct?page=1&sort=${sortType}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(name),
            }).then((res) => res.json());

            document.querySelector(".sort-select").innerHTML = response["sort"];
            if (response["total"] !== 0)
            {
                document.querySelector(".listproduct").innerHTML = response["listproduct"];
                document.querySelector(".pagination").innerHTML = response["pagination"];
            }
            else nothing.classList.remove("hidden");
            document.getElementById('loading-overlay').style.display = 'none';
            sortProduct();
            movePagination();
        });
        
    });
}


// Chuyển trang
movePagination();
function movePagination()
{
    document.querySelectorAll(".paging-btn").forEach((item) => {
        item.addEventListener("click", async(e) => {
            e.preventDefault();
            var name = document.querySelector('.name-key').textContent;
            let pageId = item.getAttribute('value');
            let sortType = document.querySelector("#sortButton.check").getAttribute('value');
            window.history.pushState('newPage', '', "/search?name=" + String(name) + "&page=" + String(pageId) + "&sort=" + String(sortType));

            document.getElementById('loading-overlay').style.display = 'flex';
            let response = await fetch(`/searchProduct?page=${pageId}&sort=${sortType}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(name),
            }).then((res) => res.json());

            document.querySelector(".listproduct").innerHTML = response["listproduct"];
            document.querySelector(".pagination").innerHTML = response["pagination"];

            var element = document.getElementById('feature1');
            if (element) {
                var topPos = element.offsetTop;
                element.scrollIntoView({ top: topPos, behavior: 'smooth' });
            }

            document.getElementById('loading-overlay').style.display = 'none';

            movePagination();
        })
    })
}


// Hiệu ứng với thanh Sort
function toggleSort() {
    var sortArrow = document.querySelector("div.sort-select > div.arrow-filter");
    let sortBlock = document.getElementById('sortBlock');


    if (sortBlock.classList.contains('hidden')) {
        sortBlock.classList.remove("hidden");
        sortArrow.classList.remove("hidden");
    }
    setTimeout(function() {
        sortBlock.classList.toggle("visible");
    }, 10);
    setTimeout(function() {
        sortArrow.classList.toggle("visible");
    }, 10);
    
    sortBlock.addEventListener('transitionend', function() {
        if (!sortBlock.classList.contains('visible')) {
            sortBlock.classList.add('hidden');
        }
    });
    
    sortArrow.addEventListener('transitionend', function() {
        if (!sortArrow.classList.contains('visible')) {
            sortArrow.classList.add('hidden');
        } 
    });
}


function openSort() {
    toggleSort();
}

function hiddenSort() {
    var sortArrow = document.querySelector("div.sort-select > div.arrow-filter");
    let sortBlock = document.getElementById('sortBlock');

    sortBlock.classList.remove("visible");
    sortArrow.classList.remove("visible");
    
    
    sortBlock.addEventListener('transitionend', function() {
        if (!sortBlock.classList.contains('visible')) {
            sortBlock.classList.add('hidden');
        }
    });
    
    sortArrow.addEventListener('transitionend', function() {
        if (!sort.classList.contains('visible')) {
            sortArrow.classList.add('hidden');
        } 
    });
}


// Thêm sự kiện click vào cả trang web để đóng phần tử 'sort-select' hoặc input-focus khi người dùng nhấn vào bất kỳ chỗ nào trên trang
document.addEventListener('click', function(event) {
    let sortSelect = document.getElementById('sortSelect');
    let sortBlock = document.getElementById('sortBlock');

    var input = document.querySelector('.t-text-field__wrapper');
    var clearIcon = document.querySelector('.t-text-field__clearable');
    if (sortSelect.contains(event.target)) {
        // Người dùng đang click vào phần tử 'sort-select' hoặc 'sortButton' hoặc 'sortBlock'
    } else {
        // Người dùng đang click vào bất kỳ chỗ nào trên trang khác, đóng phần tử 'sort-select'
        hiddenSort();
    }

    if (input.contains(event.target)) {
    } else {
        input.classList.remove('t-text-field--focused');
        clearIcon.style.display = 'none';
    }
});


// Input
const textField = document.querySelector('.t-text-field');
const input = document.querySelector('.t-text-field__wrapper');
const clearIcon = document.querySelector('.t-text-field__clearable');

clearIcon.addEventListener('click', function() {
    textField.value = ''; // Xóa nội dung của input
    console.log('hello');
    clearIcon.style.display = 'none'; // Ẩn icon sau khi xóa nội dung
    input.classList.remove('t-text-field--focused');
});

textField.addEventListener('focus', function() {
    input.classList.add('t-text-field--focused');
    if (textField.value.trim() !== '') clearIcon.style.removeProperty('display');
});

textField.addEventListener('input', function() {
    if (textField.value.trim() !== '') {
        console.log(textField.value.trim());
        if (input.classList.contains('t-text-field--focused')) clearIcon.style.removeProperty('display'); // Hiển thị icon khi có nội dung
    } else {
        clearIcon.style.display = 'none'; // Ẩn icon khi không có nội dung
    }
});
  
input.addEventListener('mouseenter', function() {
    if (textField.value.trim() !== '') clearIcon.style.removeProperty('display');
});
  
input.addEventListener('mouseleave', function() {
    if (!input.classList.contains('t-text-field--focused') || textField.value.trim() === '') 
        clearIcon.style.display = 'none';
});


// Tìm vị trí cho hộp lựa chọn bộ lọc
setInterval(function() {
    var sortSelect = document.querySelector(".sort-select");
    var sortBox = document.querySelector(".sort-select-main");
    var arrowSort = document.querySelector("div.sort-select > div.arrow-filter");
    var currentPosition = sortSelect.getBoundingClientRect();
    var midBox = currentPosition.left + (currentPosition.width - sortBox.getBoundingClientRect().width) / 2;
    var mid = (currentPosition.left + (currentPosition.width - arrowSort.getBoundingClientRect().width) / 2);

    
    if (midBox <= 0 && currentPosition.left + currentPosition.width - 10 > 0)
        sortBox.style.transform = "translate3d(" + String(0) + "px, 71.333px, 0px)";   
    else if (midBox <= 0 && currentPosition.left + currentPosition.width - 10 <= 0)
        sortBox.style.transform = "translate3d(" + String(currentPosition.left + currentPosition.width - 10) + "px, 71.333px, 0px)"; 
    else sortBox.style.transform = "translate3d(" + String(midBox) + "px, 71.333px, 0px)";       

    if (mid <= 0 && currentPosition.left + currentPosition.width - 10 > 0)
        arrowSort.style.transform = "translate3d(" + String(0) + "px, 67px, 0px) rotate(45deg)";   
    else if (mid <= 0 && currentPosition.left + currentPosition.width - 10 <= 0)
        arrowSort.style.transform = "translate3d(" + String(currentPosition.left + currentPosition.width - 10) + "px, 67px, 0px) rotate(45deg)"; 
    else arrowSort.style.transform = "translate3d(" + String(mid) + "px, 67px, 0px) rotate(45deg)";    
}, 1); 

var boxFilter = document.querySelector('.section-filter');
var sortFrame = document.querySelector('.sort-select')

// Thêm sự kiện cuộn trang
window.addEventListener('scroll', function() {
    // Kiểm tra vị trí của phần tử lớn
    var sectionFilter = document.querySelector(".section-filter");
    var currentPosition = sectionFilter.getBoundingClientRect();

    if (currentPosition.top <= 2) {
        boxFilter.classList.add('sticky');
        sortFrame.classList.add('sticky_');
    } else {
        boxFilter.classList.remove('sticky');
        sortFrame.classList.remove('sticky_');
    }
});