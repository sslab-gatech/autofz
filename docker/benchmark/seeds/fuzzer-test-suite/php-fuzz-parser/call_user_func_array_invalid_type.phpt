<?php
class drv {
    function func() {
    }
}

$drv = new drv;
try {
    call_user_func_array(array($drv, 'func'), null);
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
?>