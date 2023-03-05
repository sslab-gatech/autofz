<?php
trait A
{
    public function a(){
        echo 'Done';
    }
}
trait B
{
    use A;
}
trait C
{
    use A;
}
class D
{
    use B, C;
}

(new D)->a();