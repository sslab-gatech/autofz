<?php
function foo() {
    try {
        extract(["this"=>42, "a"=>24]);
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump($a);
}
foo();
?>