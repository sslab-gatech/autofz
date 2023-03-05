<?php
function test($a, $b){
    if ($a==10) {
        $w="x";
    } else {
        $w="y";
    }

    if ($b) {
        $d1="none";
        $d2="block";
    } else {
        $d1="block";
        $d2="none";
    }

    echo $d2.$b."\n";

}

test(1, 1);
?>