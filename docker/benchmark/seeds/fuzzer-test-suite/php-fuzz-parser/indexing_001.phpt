<?php
echo "*** Indexing - Testing value assignment with key ***\n";
$array=array(1);
$testvalues=array(null, 0, 1, true, false,'',' ',0.1,array());

foreach ($testvalues as $testvalue) {
    try {
        $testvalue['foo']=$array;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump($testvalue);
}
echo "\n*** Indexing - Testing reference assignment with key ***\n";

$testvalues=array(null, 0, 1, true, false,0.1,array());

foreach ($testvalues as $testvalue) {
    try {
        $testvalue['foo']=&$array;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump($testvalue);
}
echo "*** Indexing - Testing value assignment no key ***\n";
$array=array(1);
$testvalues=array(null, 0, 1, true, false,0.1,array());

foreach ($testvalues as $testvalue) {
    try {
        $testvalue[]=$array;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump ($testvalue);
}
echo "\n*** Indexing - Testing reference assignment no key ***\n";

$testvalues=array(null, 0, 1, true, false,0.1,array());

foreach ($testvalues as $testvalue) {
    try {
        $testvalue[]=&$array;
    } catch (Error $e) {
        echo $e->getMessage(), "\n";
    }
    var_dump ($testvalue);
}

?>