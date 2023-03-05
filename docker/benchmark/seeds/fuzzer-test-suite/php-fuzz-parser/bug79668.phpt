<?php
$df = get_defined_functions(true);
foreach (['sha1', 'sha1_file', 'hash', 'password_hash'] as $funcname) {
    var_dump(in_array($funcname, $df['internal'], true));
}
?>