<?php
function test($arg){
    throw new Exception();
}

try {
    test('ัะตัั');
}
catch(Exception $e) {
    echo $e->getTraceAsString(), "\n";
    echo (string)$e;
}
?>