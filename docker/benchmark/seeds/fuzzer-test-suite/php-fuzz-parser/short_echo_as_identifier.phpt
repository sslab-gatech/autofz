<?php
trait T {
    public function x() {}
}
class C {
    use T {
        x as y?><?= as my_echo;
    }
}
?>