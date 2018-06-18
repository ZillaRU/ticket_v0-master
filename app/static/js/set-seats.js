let stadiumData = null;
let areaData = null;

let curRows = 0;
let curCols = 0;

let curSeatStatus = 'selected';
let elseSeatStatus = 'available';

let settingSeats = false;
let settingRowCol = false;


$(document).ready(function () {
    $.ajax(
        {
            url: '/getStadium',
            type: 'get',
            dataType: 'json',
            success: function (res) {
                if (res['ret'] === 'FAILURE') {
                    alert('请求失败！');
                    return;
                }
                stadiumData = res['data'];
                let stadiums = $('#stadiums');
                $.each(stadiumData, function (i, item) {
                    stadiums.append('<option>' + item[1] + '</option>');
                });
                let curStadiumIndex = getSelectedStadiumIndex();
                if (curStadiumIndex >= 0) {
                    stadiumChanged(stadiumData[0][0]);
                }
            }
        }
    );
});

function onSelected() {
    console.log('click');
    if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
        $(this).addClass('available');
    } else if ($(this).hasClass('available')) {
        $(this).removeClass('available');
        $(this).addClass('selected');
    }
}

function getDefaultSeatMap(rows, cols) {
    curRows = rows;
    curCols = cols;

    let seatMap = $('#seat-map');
    let appendStr = '';

    let header = $('<div class="seatCharts-row seatCharts-header"></div>');
    appendStr += '<div class="seatCharts-cell"></div>';
    for (let j = 1; j <= cols; j++) {
        appendStr += '<div class="seatCharts-cell col-header">' + j + '</div>';
    }
    header.append(appendStr);
    seatMap.append(header);

    for (let i = 0; i < rows; i++) {
        let row = $('<div class="seatCharts-row"></div>');
        seatMap.append(row);
        row.append('<div class="seatCharts-cell seatCharts-space row-header">' + (i + 1) + '</div>');
        for (let j = 0; j < cols; j++) {
            let seat = $('<div class="seatCharts-seat seatCharts-cell available">' + (j + 1) + '</div>');
            seat.attr('x', i);
            seat.attr('y', j);
            // seat.attr('row-no', i + 1);
            // seat.attr('seat-no', j + 1);
            seat.click(onSelected);
            row.append(seat);
        }
    }
}

function getSelectedStadiumIndex() {
    let i = $('option:selected', '#stadiums').index();
    console.log('selected stadium index: ' + i);
    return i;
}

function getSelectedAreaIndex() {
    let i = $('option:selected', '#areas').index();
    console.log('selected area index: ' + i);
    return i;
}

function stadiumChanged(sid) {
    $.ajax(
        {
            url: '/getArea',
            type: 'get',
            data: {
                stadiumId: sid
            },
            dataType: 'json',
            success: function (res) {
                if (res['ret'] === 'FAILURE') {
                    alert('请求失败！');
                    return;
                }
                areaData = res['data'];
                let areas = $('#areas');
                areas.empty();
                $.each(areaData, function (i, item) {
                    areas.append('<option>' + item[1] + '</option>');
                });
            }
        }
    );
}

// todo
function getSeatMap() {

    let curStadiumIndex = getSelectedStadiumIndex();
    let curAreaIndex = getSelectedAreaIndex();

    if (curStadiumIndex < 0 || curAreaIndex < 0) {
        alert('请选择正确区域！');
        return;
    }

    $.ajax({
        url: '/getSeats',
        type: 'get',
        data: {
            stadiumId: stadiumData[curStadiumIndex][0],
            areaId: areaData[curAreaIndex][0]
        },
        dataType: 'json',
        success: function (res) {
            if (res['ret'] === 'FAILURE') {
                alert('请求失败！');
                return;
            }

            $('#seat-map').empty();

            let data = res['data'];
            if (data['area_status'] === 'no seat') {
                alert('该区域还没有设置座位，请开始设置～');
                $('#change-size').css('display', 'block');
                getDefaultSeatMap(30, 30);
            } else {
                // alert('该区域已设置过座位。'); todo 已经设置过的怎么修改？？？感觉还是不要允许删除和修改现有座位了，要改就整个区域的座位都删掉好了。。。
                /* todo 没写，待完成
                $.each(data['seat_list'], function (i, seat) {

                });
                */
            }
        }
    });
}

$('#stadiums').change(function () {
    let i = getSelectedStadiumIndex();
    // console.log('selected: ' + stadiumData[i][1] + ', stadiumId = ' + stadiumData[i][0]);
    stadiumChanged(stadiumData[i][0]);
});

$('#areas').change(function () {
    getSelectedAreaIndex();
});

function addRowCount() {
    let addRowCount = parseInt($('#additional-row-count').val());
    let seatMap = $('#seat-map');

    for (let i = curRows; i < curRows + addRowCount; i++) {
        let row = $('<div class="seatCharts-row"></div>');
        seatMap.append(row);
        row.append('<div class="seatCharts-cell seatCharts-space row-header">' + (i + 1) + '</div>');
        for (let j = 0; j < curCols; j++) {
            let seat = $('<div class="seatCharts-seat seatCharts-cell available">' + (j + 1) + '</div>');
            seat.attr('x', i);
            seat.attr('y', j);
            // seat.attr('row-no', i + 1);
            // seat.attr('seat-no', j + 1);
            seat.click(onSelected);
            row.append(seat);
        }
    }
    curRows += addRowCount;
}

function addColCount() {
    let addColCount = parseInt($('#additional-col-count').val());
    let appendStr = '';
    $('.seatCharts-row').each(function (i, item) {
        if ($(this).hasClass('seatCharts-header')) {
            for (let j = curCols; j < curCols + addColCount; j++) {
                $(this).append('<div class="seatCharts-cell">' + (j + 1) + '</div>');
            }
        } else {
            for (let j = curCols; j < curCols + addColCount; j++) {
                let seat = $('<div class="seatCharts-seat seatCharts-cell available">' + (j + 1) + '</div>');
                seat.attr('x', i);
                seat.attr('y', j);
                // seat.attr('row-no', i + 1);
                // seat.attr('seat-no', j + 1);
                seat.click(onSelected);
                $(this).append(seat);
            }
        }
    });
    curCols += addColCount;
}

function seatsFinished() {
    settingSeats = false;
}

function setRowCol() {
    if (settingRowCol === true) return;
    settingSeats = false;
    settingRowCol = true;

    // set row
    $('.row-header').each(function () {
        let a = $(this).html();
        $(this).html('<input class="cell-input" type="text" value="' + a + '"/>');
    });

    // set col
    $('.col-header').each(function () {
        let a = $(this).html();
        $(this).html('<input class="cell-input" type="text" value="' + a + '"/>');
    });
}

function rowColFinished() {
    if (settingRowCol === false) return;
    settingRowCol = false;

    // row finished
    $('.row-header').each(function () {
        let a = $(this).find('input').val();
        $(this).html(a);
    });

    // col finished
    $('.col-header').each(function () {
        let a = $(this).find('input').val();
        $(this).html(a);
    });
}

//

function setStatus(newStatus) {
    curSeatStatus = newStatus;
    if (newStatus === 'selected') {
        elseSeatStatus = 'available';
    }
    else {
        elseSeatStatus = 'selected';
    }
}

function setSeats() {
    if (settingSeats === true) return;
    settingSeats = true;
    rowColFinished();
}

function constructSeat(x, y, rowNo, seatNo) {
    this.x = x;
    this.y = y;
    this.rowNo = rowNo;
    this.seatNo = seatNo;
    return this;
}

function constructSeatList() {
    seatsFinished();
    rowColFinished();

    console.log('constructSeatList');

    let seatList = [];

    let rowHeader = new Array(curRows);
    let colHeader = new Array(curCols);

    $('.row-header').each(function (i) {
        rowHeader[i] = $(this).html();
    });
    $('.col-header').each(function (i) {
        colHeader[i] = $(this).html();
    });

    $('.selected').each(function () {
        let x = $(this).attr('x');
        let y = $(this).attr('y');
        let seat = constructSeat(x, y, rowHeader[x], colHeader[y]);
        seatList.push(seat);
    });

    console.log("length: " + seatList.length);
/*
    for (let i = 0; i < seatList.length; i++) {
        console.log(seatList[i]);
    }
*/
    return seatList;
}
