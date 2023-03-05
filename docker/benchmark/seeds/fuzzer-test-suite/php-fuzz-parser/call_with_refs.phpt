<?php
class Test {
    public function __toString() {
        global $my_var;
        $my_var=0x12345;
        return "";
    }
}

$my_var = str_repeat("A",64);
$data = call_user_func_array("substr_replace",array(&$my_var, new Test(), 1));
echo "OK!";
?>