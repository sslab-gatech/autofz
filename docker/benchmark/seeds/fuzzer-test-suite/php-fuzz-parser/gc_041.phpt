<?php
class ryat {
        var $ryat;
        var $chtg;
        var $nested;
        function __destruct() {
                $GLOBALS['x'] = $this;
        }
}
$o = new ryat;
$o->nested = [];
$o->nested[] =& $o->nested;
$o->ryat = $o;
$x =& $o->chtg;
unset($o);
var_dump(gc_collect_cycles());
var_dump($x);
?>