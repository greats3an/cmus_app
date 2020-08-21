function parseTime(s) {
    return new Date(s * 1000).toISOString().substr(14,5)
}
function runCommand(command) {
    $.ajax({
        type: 'POST', url: 'cmd', data: { command: command }, context: $("div#result"),
        error: function () {
            var msg = '<p class="red label"><i class="icon-remove"></i> ' + command + '</p>';
            this.html(msg)
        },
        success: function () {
            var msg = '<p class="green label"><i class="icon-ok"></i> ' + command + '</p>'
            this.html(msg)
        }
    })
}
function updateStatus() {
    $.ajax({
        url: 'status', dataType: 'json', context: $("div#status"),
        error: function () {
            var msg = '<p class="error">Connection to <code>cmus</code> cannot be established.</p>';
            this.html(msg)
        },
        success: function (response) {
            if (response.status[0] == "playing") { var msg = '<p>' } else { var msg = '<p class="gray">' }
            mask = (response.tag.artist != null)  << 3 | (response.tag.title != null) << 2 | (response.tag.album != null) << 1 | (response.tag.date != null) << 0
            switch (mask) {
                case parseInt(1111, 2): // artist,title,album,date
                    msg += response.tag.artist + ': <strong>' + response.tag.title + '</strong> (' + response.tag.album + ', ' + response.tag.date.substring(0, 4) + ')'; break
                case parseInt(1110, 2): // artist,title,album
                    msg += response.tag.artist + ': <strong>' + response.tag.title + '</strong> (' + response.tag.album + ')'; break
                case parseInt(1101, 2): // artist,title,date
                    msg += response.tag.artist + ': <strong>' + response.tag.title + '</strong> (' + response.tag.date.substring(0, 4) + ')'; break
                case parseInt(1100, 2): // artist,title
                    msg += response.tag.artist + ': <strong>' + response.tag.title + '</strong>'; break
                case parseInt(0100, 2): // title
                    msg += '<strong>' + response.tag.title + '</strong>'; break
                case parseInt(1000, 2): // artist
                    msg += response.tag.artist + ': <strong>(unknown)</strong>'; break
                default:                // none
                    msg += '<em>none/unknown</em>'
            }
            msg += '</p><span class="vol gray">';
            if (response.set.vol_left != null) { msg += response.set.vol_left }
            if (response.set.shuffle == 'true') { msg += ' <i class="icon-random"></i>' }
            if (response.set.repeat == 'true') { msg += ' <i class="icon-refresh"></i>' }
            msg += '</span></br>';
            msg += '<progress max="' + response.duration[0] + '" value="' + response.position[0] + '"></progress>';
            msg += parseTime(response.position[0]) + ' / ' + parseTime(response.duration[0])
            this.html(msg)
        }
    })
}
$(".cmd-btn").on('click', (function () {
    var cmd = $(this).attr('title');
    runCommand(cmd);
    updateStatus();
}))
$("div#result").on('click', (function () {
    $(this).empty()
}))
setInterval(updateStatus, 1000) // update per sec