// Xử lý bất đồng bộ
document.addEventListener("DOMContentLoaded", async(e) =>  {
    document.getElementById('loading-overlay').style.display = 'flex';
    let response = await fetch(`/filterProduct?c=${category}&page=1&sort=1`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(currentFilters),
    }).then((res) => res.json());

    document.querySelector(".sort-select").innerHTML = response["sort"];
    if (response["total"] !== 0)
    {
        document.querySelector(".listproduct").innerHTML = response["listproduct"];
        document.querySelector(".pagination").innerHTML = response["pagination"];
    }
    document.getElementById('loading-overlay').style.display = 'none';
    sortProduct();
    movePagination();
});


// Load lại trang
let category = window.location.pathname;
var categories = category.split('/');
category = categories[1];
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, String(category));
}


// Section filter
function getElementPosition(element) {
    return element.getBoundingClientRect();
}

// Tìm vị trí cho hộp lựa chọn bộ lọc
setInterval(function() {
    document.querySelectorAll(".filter-parameter").forEach((filterName) => { 
        var screenWidth = window.innerWidth;
        var currentPosition = getElementPosition(filterName);

        var filterBox = filterName.querySelector(".filter-value-box");
        var arrowFilter = filterName.querySelector(".arrow-filter");
        var filterBoxRect = getElementPosition(filterBox);
        var arrowFilterRect = getElementPosition(arrowFilter);
 
        if (currentPosition.left - 50 + filterBoxRect.width >= screenWidth && currentPosition.left + 10 < screenWidth)
            filterBox.style.transform = "translate3d(" + String(screenWidth - filterBoxRect.width) + "px, 71.333px, 0px)";   
        else if (currentPosition.left - 50 + filterBoxRect.width >= screenWidth && currentPosition.left + 10 >= screenWidth)
            filterBox.style.transform = "translate3d(" + String(currentPosition.left - filterBoxRect.width + 10) + "px, 71.333px, 0px)"; 
        else if (currentPosition.left - 50 <= 0 && currentPosition.left + currentPosition.width - 10 > 0)
            filterBox.style.transform = "translate3d(" + String(0) + "px, 71.333px, 0px)";   
        else if (currentPosition.left - 50 <= 0 && currentPosition.left + currentPosition.width - 10 <= 0)
            filterBox.style.transform = "translate3d(" + String(currentPosition.left + currentPosition.width - 10) + "px, 71.333px, 0px)"; 
        else filterBox.style.transform = "translate3d(" + String(currentPosition.left - 50) + "px, 71.333px, 0px)";    

        if (currentPosition.left + 20 + arrowFilterRect.width >= screenWidth && currentPosition.left + 20 < screenWidth)
            arrowFilter.style.transform = "translate3d(" + String(screenWidth - arrowFilterRect.width) + "px, 67px, 0px) rotate(45deg)";   
        else if (currentPosition.left + 20 + arrowFilterRect.width >= screenWidth && currentPosition.left + 20 >= screenWidth)
            arrowFilter.style.transform = "translate3d(" + String(currentPosition.left + 20 - arrowFilterRect.width) + "px, 67px, 0px) rotate(45deg)"; 
        else if (currentPosition.left + 20 <= 0 && currentPosition.left + currentPosition.width - 20 > 0)
            arrowFilter.style.transform = "translate3d(" + String(0) + "px, 67px, 0px) rotate(45deg)";   
        else if (currentPosition.left + 20 <= 0 && currentPosition.left + currentPosition.width - 20 <= 0)
            arrowFilter.style.transform = "translate3d(" + String(currentPosition.left + currentPosition.width - 20) + "px, 67px, 0px) rotate(45deg)"; 
        else arrowFilter.style.transform = "translate3d(" + String(currentPosition.left + 20) + "px, 67px, 0px) rotate(45deg)";    
    });

    var sortSelect = document.querySelector(".sort-select");
    var sortBox = document.querySelector(".sort-select-main");
    var arrowSort = document.querySelector("div.sort-select > div.arrow-filter");
    var currentPosition = getElementPosition(sortSelect);
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

    			
    document.querySelectorAll(".filter-parameter-name").forEach((parameterItem) => {		
        if (currentPosition.top <= 2) {		
            parameterItem.classList.add('sticky_');		
        } else {		
            parameterItem.classList.remove('sticky_');		
        }		
    });
});

// Hiệu ứng với thanh sort
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
        // Không làm gì cả
    } else {
        input.classList.remove('t-text-field--focused');
        clearIcon.style.display = 'none';
    }
});


// Cập nhật Filter
function toggleFilterBox(parameterNameItem) {
    let currentBox = parameterNameItem.parentNode.querySelector(".filter-value-box");
    let currentArrow = parameterNameItem.parentNode.querySelector(".arrow-filter");
    
    parameterNameItem.classList.toggle("check");
    visitFilterValue();
    if (currentBox.classList.contains('hidden')) {
        currentBox.classList.remove("hidden");
        currentArrow.classList.remove("hidden");
    }
    setTimeout(function() {
        currentBox.classList.toggle("visible");
    }, 10);
    setTimeout(function() {
        currentArrow.classList.toggle("visible");
    }, 10);

    currentBox.addEventListener('transitionend', function() {
        if (!currentBox.classList.contains('visible')) {
            currentBox.classList.add('hidden');
        }
    });

    currentArrow.addEventListener('transitionend', function() {
        if (!currentArrow.classList.contains('visible')) {
            currentArrow.classList.add('hidden');
        } 
    });
    hiddenSort();
}


let currentCheck = null;
let filters = {};
let currentFilters = {};
document.querySelectorAll(".filter-parameter").forEach((parameterItem) => {
    let parameterNameItem = parameterItem.querySelector(".filter-parameter-name");
    parameterNameItem.addEventListener("click", (e) =>
    {
        e.preventDefault();
        if (currentCheck !== parameterNameItem)
            remove_check(e);
        
        visitFilterValue();
        currentCheck = parameterNameItem;
        e.stopPropagation();
        e.stopImmediatePropagation();

        toggleFilterBox(parameterNameItem);
    })

    let parameterName = parameterNameItem.textContent.trim();
    filters[parameterName] = new Set();

    parameterItem.querySelectorAll(".filter-value").forEach((item) => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            item.classList.toggle("check");
            visitFilterValue();
            let parameterValue = item.innerHTML;
            if (item.classList.contains("check"))
            {
                filters[parameterName].add(parameterValue);
            } else
            {
                filters[parameterName].delete(parameterValue);
            }

            let changeEvent = new Event('change');
            document.querySelector("div.box-filter").dispatchEvent(changeEvent);
            e.stopPropagation();
        });
    });    
});

visitFilterValue();
function visitFilterValue() {
    let generalCount = 0;
    document.querySelectorAll(".filter-parameter").forEach((parameterItem) => {
        let count = 0;
        let parameterNameItem = parameterItem.querySelector(".filter-parameter-name");
        parameterItem.querySelectorAll(".filter-value").forEach((item) => {
            if (item.classList.contains("check")) {
                count += 1;
                generalCount += 1;
            }
        });
        if (count > 0) parameterNameItem.classList.add("check");
    });

    document.querySelectorAll(".filter-button").forEach((filterButton) => {
        if (generalCount > 0) {
            filterButton.classList.remove("hidden");
            setTimeout(function() {
                filterButton.classList.add("visible");
            }, 10);
        } else {
            filterButton.classList.remove("visible");
            setTimeout(function() {
                filterButton.classList.add("hidden");
            }, 10);
        }
    });
    
}


function remove_check(e) {
    if (currentCheck)
    {
        let currentBox = currentCheck.parentNode.querySelector(".filter-value-box");
        let currentArrow = currentCheck.parentNode.querySelector(".arrow-filter");

        currentCheck.classList.remove("check");
        currentBox.classList.remove("visible");
        currentArrow.classList.remove("visible");

        currentBox.addEventListener('transitionend', function() {
            if (!currentBox.classList.contains('visible')) {
              currentBox.classList.add('hidden');
            }
        });

        currentArrow.addEventListener('transitionend', function() {
            if (!currentArrow.classList.contains('visible')) {
              currentArrow.classList.add('hidden');
            }
        });

        currentCheck = null;
        visitFilterValue();
    }
}
document.addEventListener("click", remove_check);
document.querySelectorAll(".filter-value-box").forEach((item)=>{
    item.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
    })
});


// Thay đổi filter và chạy bất đồng bộ
document.querySelector("div.box-filter").addEventListener("change", async(e) => {
    e.preventDefault();
    for (let key in filters)
    {
        currentFilters[key] = Array.from(filters[key]);
    }

    document.querySelectorAll(".submit").forEach((submitButton) => {
        submitButton.classList.add('prevent');
        submitButton.innerHTML = 'Xem <b class="total-reloading"><div class="stage-two"><div class="load"></div></div></b> kết quả</a>';
    });

    let response = await fetch(`/filterProduct?c=${category}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(currentFilters),
    }).then((res) => res.json());

    document.querySelectorAll(".submit").forEach((submitButton) => {
        submitButton.innerHTML = `Xem <b class="product-search-number">${response["total"]}</b> kết quả`;
        submitButton.classList.remove('prevent');
        if (response["total"] === 0) {
            submitButton.classList.add('disable');
        }
        else {
            submitButton.classList.remove('disable');
        }
    });
});


// Sắp xếp sản phẩm 
sortProduct();
function sortProduct() {

    document.querySelectorAll("#sortButton").forEach((sortButton) => {
        sortButton.addEventListener("click", async(e) => {
            let sortType = sortButton.getAttribute('value');

            e.stopPropagation();
            e.stopImmediatePropagation();
            e.preventDefault();

            window.history.pushState('newSort', '', String(category) + "?page=1&sort=" + String(sortType));
            document.getElementById('loading-overlay').style.display = 'flex';
            let response = await fetch(`/filterProduct?c=${category}&page=1&sort=${sortType}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(currentFilters),
            }).then((res) => res.json());

            document.querySelector(".sort-select").innerHTML = response["sort"];
            if (response["total"] !== 0)
            {
                document.querySelector(".listproduct").innerHTML = response["listproduct"];
                document.querySelector(".pagination").innerHTML = response["pagination"];
            }
            document.getElementById('loading-overlay').style.display = 'none';
            sortProduct();
            movePagination();
        });
        
    });
}

// Xóa bộ lọc
document.querySelectorAll("div.filter-close").forEach((closeButton) => {
    closeButton.addEventListener("click", (e) => {

        document.querySelectorAll(".filter-parameter").forEach((parameterItem) => {
            let parameterNameItem = parameterItem.querySelector(".filter-parameter-name");
            let parameterName = parameterNameItem.textContent.trim();
            parameterItem.querySelectorAll(".filter-value").forEach((item) => {
                item.classList.remove("check");
                let parameterValue = item.innerHTML;
                filters[parameterName].delete(parameterValue);
            });     
            parameterNameItem.classList.remove('check');
        });
        remove_check(e);
    });
});


// Submit Filter
searchProduct();
function searchProduct() {
    document.querySelectorAll("div.submit").forEach((submit) => {
        submit.addEventListener("click", async(e) => {
            e.preventDefault();
            remove_check(e);

            let sortType = document.querySelector("#sortButton.check").getAttribute('value');
            window.history.pushState('newSearch', '', String(category) + "?page=1&sort=" + String(sortType));
            document.getElementById('loading-overlay').style.display = 'flex';
            let response = await fetch(`/filterProduct?c=${category}&page=1&sort=${sortType}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(currentFilters),
            }).then((res) => res.json());
        
            if (response["total"] !== 0)
            {
                document.querySelector(".listproduct").innerHTML = response["listproduct"];
                document.querySelector(".pagination").innerHTML = response["pagination"];
            }
            document.getElementById('loading-overlay').style.display = 'none';
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
            let pageId = item.getAttribute('value');
            let sortType = document.querySelector("#sortButton.check").getAttribute('value');
            window.history.pushState('newPage', '', String(category) + "?page=" + String(pageId) + "&sort=" + String(sortType));

            document.getElementById('loading-overlay').style.display = 'flex';
            let response = await fetch(`/filterProduct?c=${category}&page=${pageId}&sort=${sortType}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(currentFilters),
            }).then((res) => res.json());

            document.querySelector(".listproduct").innerHTML = response["listproduct"];
            document.querySelector(".pagination").innerHTML = response["pagination"];

            var element = document.getElementById('form');
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }

            document.getElementById('loading-overlay').style.display = 'none';

            movePagination();
        })
    })
}


// Input
const textField = document.querySelector('.t-text-field');
const input = document.querySelector('.t-text-field__wrapper');
const clearIcon = document.querySelector('.t-text-field__clearable');

clearIcon.addEventListener('click', function() {
    textField.value = ''; // Xóa nội dung của input
    clearIcon.style.display = 'none'; // Ẩn icon sau khi xóa nội dung
    input.classList.remove('t-text-field--focused');
});

textField.addEventListener('focus', function() {
    input.classList.add('t-text-field--focused');
    if (textField.value.trim() !== '') clearIcon.style.removeProperty('display');
});

textField.addEventListener('input', function() {
    if (textField.value.trim() !== '') {
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