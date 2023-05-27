// Input
document.addEventListener('click', function(event) {
    var input = document.querySelector('.t-text-field__wrapper');
    var clearIcon = document.querySelector('.t-text-field__clearable');

    if (input.contains(event.target)) {
    } else {
        input.classList.remove('t-text-field--focused');
        clearIcon.style.display = 'none';
    }
});


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
