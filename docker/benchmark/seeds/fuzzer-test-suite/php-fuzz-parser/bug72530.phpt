<?php

class ryat {
    var $ryat;
    var $chtg;

    function __destruct() {
        $this->chtg = $this->ryat;
        $this->ryat = 1;
    }
}

$o = new ryat;
$o->ryat = $o;
$x =& $o->chtg;

unset($o);
gc_collect_cycles();
var_dump($x);

?>