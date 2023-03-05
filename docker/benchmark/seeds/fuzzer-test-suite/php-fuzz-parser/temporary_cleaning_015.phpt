<?php
set_error_handler(function () {
    throw new Exception();
});
$a = [];
$b = "";
try {
     echo "$a$b\n";
} catch (Exception $ex) {
}
?>
DONE