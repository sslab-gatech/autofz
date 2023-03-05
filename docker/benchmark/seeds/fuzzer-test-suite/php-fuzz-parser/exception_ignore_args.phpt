<?php
$function = function(string $user, string $pass) {
    throw new Exception();
};

ini_set("zend.exception_ignore_args", 1);

$function("secrets", "arewrong");
?>