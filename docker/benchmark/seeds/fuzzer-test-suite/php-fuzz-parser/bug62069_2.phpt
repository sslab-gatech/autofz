<?php

trait T1 {
    public function func() {
        echo "From T1\n";
    }
}

trait T2 {
    public function func() {
        echo "From T2\n";
    }
}

class Bar {
    public function func() {
        echo "From Bar\n";
    }
    use T1 {
        func as f1;
    }
    use T2 {
        func as f2;
    }
}

$b = new Bar();
$b->f2();

?>