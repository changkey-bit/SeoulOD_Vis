document.addEventListener("DOMContentLoaded", function() {
    const resetButton = document.getElementById('resetBtn');

    // 리셋 버튼에 클릭 이벤트 리스너를 추가합니다.
    resetButton.addEventListener('click', function() {
        // 모든 체크박스를 선택 해제합니다.
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = false;
        });

        // select box를 첫 번째 값으로 초기화합니다.
        const selectBoxes = document.querySelectorAll('select');
        selectBoxes.forEach(function(selectBox) {
            selectBox.selectedIndex = 0;
        });
    });
});