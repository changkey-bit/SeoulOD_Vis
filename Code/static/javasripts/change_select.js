const select_heat = document.getElementById('dist_data1');
const select_flow = document.getElementById('dist_data2');

const select_heat_cri = document.getElementById('criteria_data1');
const select_flow_cri = document.getElementById('criteria_data2');

// 첫 번째 select 요소의 변경 이벤트에 대한 리스너를 추가합니다.
select_heat.addEventListener('change', function () {
    // 선택한 옵션의 값(value)을 가져옵니다.
    const selectedValue_heat = select_heat.value;
    const previousSelectedValue_heat_cri = select_heat_cri.value;

    // 두 번째 select 요소를 초기화합니다.
    select_heat_cri.innerHTML = '';

    // 선택한 값에 따라 두 번째 select 요소의 옵션을 설정합니다.
    if (selectedValue_heat === 'personcount') {
        select_heat_cri.add(new Option('--- 선택안함 ---', '선택안함'));
        select_heat_cri.add(new Option('100', '100'));
        select_heat_cri.add(new Option('500', '500'));
        select_heat_cri.add(new Option('1,000', '1000'));
        select_heat_cri.add(new Option('10,000', '10000'));
        select_heat_cri.add(new Option('50,000', '50000'));
        select_heat_cri.add(new Option('60,000', '60000'));
        select_heat_cri.add(new Option('70,000', '70000'));
        select_heat_cri.add(new Option('80,000', '80000'));
        select_heat_cri.add(new Option('90,000', '90000'));
        select_heat_cri.add(new Option('100,000', '100000'));
        select_heat_cri.add(new Option('150,000', '150000'));
        select_heat_cri.add(new Option('200,000', '200000'));
        select_heat_cri.add(new Option('250,000', '250000'));
        select_heat_cri.add(new Option('300,000', '300000'));
        select_heat_cri.add(new Option('350,000', '300000'));

    } else if (selectedValue_heat === 'dist') {
        select_heat_cri.add(new Option('--- 선택안함 ---', '선택안함'));
        select_heat_cri.add(new Option('10,000', '10000'));
        select_heat_cri.add(new Option('50,000', '50000'));
        select_heat_cri.add(new Option('100,000', '100000'));
        select_heat_cri.add(new Option('150,000', '150000'));
        select_heat_cri.add(new Option('200,000', '200000'));
        select_heat_cri.add(new Option('250,000', '250000'));
        select_heat_cri.add(new Option('300,000', '300000'));
        select_heat_cri.add(new Option('350,000', '350000'));
        select_heat_cri.add(new Option('400,000', '400000'));
        select_heat_cri.add(new Option('450,000', '450000'));

    } else if (selectedValue_heat === 'ttime') {
        select_heat_cri.add(new Option('--- 선택안함 ---', '선택안함'));
        select_heat_cri.add(new Option('10', '10'));
        select_heat_cri.add(new Option('30', '30'));
        select_heat_cri.add(new Option('60', '60'));
        select_heat_cri.add(new Option('80', '80'));
        select_heat_cri.add(new Option('100', '100'));
        select_heat_cri.add(new Option('120', '120'));
        select_heat_cri.add(new Option('140', '140'));
        select_heat_cri.add(new Option('160', '160'));
        select_heat_cri.add(new Option('180', '180'));
        select_heat_cri.add(new Option('200', '200'));
    }
        // 이전에 선택한 값이 존재하면, 해당 값을 선택합니다.
    if (previousSelectedValue_heat_cri !== '') {
        select_heat_cri.value = previousSelectedValue_heat_cri;
    }
});

// 페이지 로드 시 초기화를 위해 한 번 실행합니다.
select_heat.dispatchEvent(new Event('change'));


select_flow.addEventListener('change', function () {
    // 선택한 옵션의 값(value)을 가져옵니다.
    const selectedValue_flow = select_flow.value;
    const previousSelectedValue_flow_cri = select_flow_cri.value;


    // 두 번째 select 요소를 초기화합니다.
    select_flow_cri.innerHTML = '';

    // 선택한 값에 따라 두 번째 select 요소의 옵션을 설정합니다.
    if (selectedValue_flow === 'personcount') {
        select_flow_cri.add(new Option('--- 선택안함 ---', '선택안함'));
        select_flow_cri.add(new Option('100', '100'));
        select_flow_cri.add(new Option('300', '300'));
        select_flow_cri.add(new Option('500', '500'));
        select_flow_cri.add(new Option('700', '700'));
        select_flow_cri.add(new Option('800', '800'));
        select_flow_cri.add(new Option('1,000', '1000'));
        select_flow_cri.add(new Option('2,000', '2000'));
        select_flow_cri.add(new Option('3,000', '3000'));
        select_flow_cri.add(new Option('4,000', '4000'));
        select_flow_cri.add(new Option('5,000', '5000'));
        select_flow_cri.add(new Option('6,000', '6000'));
        select_flow_cri.add(new Option('7,000', '7000'));
        select_flow_cri.add(new Option('8,000', '8000'));
        select_flow_cri.add(new Option('9,000', '9000'));
        select_flow_cri.add(new Option('10,000', '10000'));
        select_flow_cri.add(new Option('15,000', '15000'));
        select_flow_cri.add(new Option('20,000', '20000'));
        select_flow_cri.add(new Option('25,000', '25000'));
        select_flow_cri.add(new Option('30,000', '30000'));
        select_flow_cri.add(new Option('35,000', '35000'));
        select_flow_cri.add(new Option('40,000', '40000'));
        select_flow_cri.add(new Option('45,000', '45000'));
        select_flow_cri.add(new Option('50,000', '50000'));
        select_flow_cri.add(new Option('55,000', '55000'));
        select_flow_cri.add(new Option('60,000', '60000'));
        select_flow_cri.add(new Option('65,000', '65000'));
        select_flow_cri.add(new Option('70,000', '70000'));
        select_flow_cri.add(new Option('75,000', '75000'));
        select_flow_cri.add(new Option('80,000', '80000'));
        select_flow_cri.add(new Option('85,000', '85000'));
        select_flow_cri.add(new Option('90,000', '90000'));
        select_flow_cri.add(new Option('95,000', '95000'));
        select_flow_cri.add(new Option('100,000', '100000'));

    } else if (selectedValue_flow === 'versus_time') {
        select_flow_cri.add(new Option('--- 선택안함 ---', '선택안함'));
        select_flow_cri.add(new Option('0.01', '0.01'));
        select_flow_cri.add(new Option('0.05', '0.05'));
        select_flow_cri.add(new Option('0.1', '0.1'));
        select_flow_cri.add(new Option('0.2', '0.2'));
        select_flow_cri.add(new Option('0.3', '0.3'));
        select_flow_cri.add(new Option('0.4', '0.4'));
        select_flow_cri.add(new Option('0.5', '0.5'));
        select_flow_cri.add(new Option('0.6', '0.6'));
        select_flow_cri.add(new Option('0.7', '0.7'));
        select_flow_cri.add(new Option('0.8', '0.8'));
        select_flow_cri.add(new Option('0.9', '0.9'));
        select_flow_cri.add(new Option('1.0', '1.0'));
        select_flow_cri.add(new Option('1.5', '1.5'));
        select_flow_cri.add(new Option('2.0', '2.0'));
    } 
    else if (selectedValue_flow === 'dist') {
        select_flow_cri.add(new Option('--- 선택안함 ---', '선택안함'));
        select_flow_cri.add(new Option('10,000', '10000'));
        select_flow_cri.add(new Option('50,000', '50000'));
        select_flow_cri.add(new Option('100,000', '100000'));
        select_flow_cri.add(new Option('150,000', '150000'));
        select_flow_cri.add(new Option('200,000', '200000'));
        select_flow_cri.add(new Option('250,000', '250000'));
        select_flow_cri.add(new Option('300,000', '300000'));
        select_flow_cri.add(new Option('350,000', '350000'));
        select_flow_cri.add(new Option('400,000', '400000'));
        select_flow_cri.add(new Option('450,000', '450000'));

    } else if (selectedValue_flow === 'ttime') {
        select_flow_cri.add(new Option('--- 선택안함 ---', '선택안함'));
        select_flow_cri.add(new Option('10', '10'));
        select_flow_cri.add(new Option('30', '30'));
        select_flow_cri.add(new Option('60', '60'));
        select_flow_cri.add(new Option('80', '80'));
        select_flow_cri.add(new Option('100', '100'));
        select_flow_cri.add(new Option('120', '120'));
        select_flow_cri.add(new Option('140', '140'));
        select_flow_cri.add(new Option('160', '160'));
        select_flow_cri.add(new Option('180', '180'));
        select_flow_cri.add(new Option('200', '200'));
    }
        // 이전에 선택한 값이 존재하면, 해당 값을 선택합니다.
    if (previousSelectedValue_flow_cri !== '') {
        previousSelectedValue_flow_cri.value = previousSelectedValue_flow_cri;
    }
});

// 페이지 로드 시 초기화를 위해 한 번 실행합니다.
select_flow.dispatchEvent(new Event('change'));