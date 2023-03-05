<?php

trait T1 {
    public int $prop;
}
trait T2 {
    public string $prop;
}
class C {
    use T1, T2;
}
?>