<?php
$comparator = null;
try {
    var_dump(call_user_func([$comparator, 'compare'], 1, 2));
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
?>