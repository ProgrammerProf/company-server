let _titles_ = [];
let _data_ = [];

function _delete_ (id) {

    _data_ = _data_.filter(_ => _[0] !== id);
    _set_();

}
function _insert_ (row) {

    if ( _data_.filter(_ => _[0] === parseInt(row[0]) ).length ) return;
    _data_.unshift(row);
    _set_();

}
function _set_ () {

    let table = `
        <table class="dataTable-table">
            <thead>
                <tr>
                    ${_titles_.map(_ => `<th><a class="dataTable-sorter">${text(_)}</a></th>`)}
                    <th><a>${text('actions')}</a></th>
                </tr>
            </thead>
            <tbody>
                ${
                    _data_.map((item) =>`
                        <tr>
                            ${
                                item.slice(1).map(_ =>
                                    _.toString().includes('~') ? `
                                        <td>
                                            <a href="/edit-product/${item.slice(0, 1)}" class="pointer image for-ar hover:underline hover:text-primary">
                                                <div class="bg-white-dark/30 layer-div"><img src="${_.split("~")[0]}"></div>
                                                <span class="font-semibold">${_.split("~").slice(1).join("~").slice(0, 30)}...</span>
                                            </a>
                                        </td>
                                    ` : `<td><a>${_}</a></td>`
                                )
                            }
                            <td class="buttons gap-4">
                                <button class="btn btn-sm btn-outline-danger" onclick="_delete_(${item[0]})">${text('delete')}</button>
                            </td>
                        </tr>
                    `)
                }
            </tbody>
        </table>
        ${!_data_.length ? `<div class='empty'>${text('no_systems')}</div>` : ''}
    `;

    $(".table").html(table.replace(/,/g, ''));

}
function _get_ () {

    return _data_.map(_ => _[0]);

}
function _table_ () {
    
    let data = JSON.parse($("#data-table").text());
    if ( !data ) return;

    _titles_ = data.titles || [];
    _data_ = data.data || [];
    _set_();

}
