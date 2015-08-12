<?php


/***************真实调用时，需要根据不同接口修改下面的参数*********************************/
/***************此处以DescribeInstances为例说明 如何获取指定 instanceId 的虚拟机**********/

$HttpUrl="cdn.api.qcloud.com";

/*除非有特殊说明，如MultipartUploadVodFile，其它接口都支持GET及POST*/
$HttpMethod="POST";

/*是否https协议，大部分接口都必须为https，只有少部分接口除外（如MultipartUploadVodFile）*/
$isHttps =true;

/*需要填写你的密钥，可从  https://console.qcloud.com/capi 获取 SecretId 及 $secretKey*/
$secretKey='YOUR_SECRET_KEY';


/*下面这五个参数为所有接口的 公共参数；对于某些接口没有地域概念，则不用传递Region（如DescribeDeals）*/
$COMMON_PARAMS = array(
                'Nonce' => rand(),
                'Timestamp' =>time(NULL),
                'Action' =>'GetHostInfoById',
                'SecretId' => 'YOUR_SECRET_ID',
                );

/*下面这两个参数为 DescribeInstances 接口的私有参数，用于查询特定的虚拟机列表*/
$PRIVATE_PARAMS = array(
                "ids.0" => 253,
                "ids.1" => 326,
                //"ids.2" => 335,
                //"ids.3" => 518,
                //"ids.4" => 551,
                //"ids.5" => 847,
                //"ids.6" => 862,
                //"ids.7" => 2069,
                //"ids.8" => 3731,
                //"ids.9" => 5829,
                //"ids.10" => 6097,
                //"ids.11" => 6098,
                //"ids.12" => 6612,
                //"ids.13" => 6613,
                //"ids.14" => 6614,
                //"ids.15" => 7105,
                //"ids.16" => 7394,
                //"ids.17" => 8080,
                //"ids.18" => 8106,
                //"ids.19" => 9811,
                //"ids.20" => 9812,
                //"ids.21" => 11155,
                //"ids.22" => 11639,
                //"ids.23" => 13368,
                //"ids.24" => 13443,
                //"ids.25" => 13453,
                //"ids.26" => 14746,
                //"ids.27" => 15757,
                //"ids.28" => 17209,
                //"ids.29" => 17219,
                //"ids.30" => 17326,
                //"ids.31" => 17327,
                //"ids.32" => 18422,
                //"ids.33" => 22734,
                );

/***********************************************************************************/


CreateRequest($HttpUrl,$HttpMethod,$COMMON_PARAMS,$secretKey, $PRIVATE_PARAMS, $isHttps);

function CreateRequest($HttpUrl,$HttpMethod,$COMMON_PARAMS,$secretKey, $PRIVATE_PARAMS, $isHttps)
{
        $FullHttpUrl = $HttpUrl."/v2/index.php";

        /***************对请求参数 按参数名 做字典序升序排列，注意此排序区分大小写*************/
        $ReqParaArray = array_merge($COMMON_PARAMS, $PRIVATE_PARAMS);
        ksort($ReqParaArray);

        /**********************************生成签名原文**********************************
         * 将 请求方法, URI地址,及排序好的请求参数  按照下面格式  拼接在一起, 生成签名原文，此请求中的原文为 
         * GETcvm.api.qcloud.com/v2/index.php?Action=DescribeInstances&Nonce=345122&Region=gz
         * &SecretId=AKIDz8krbsJ5yKBZQ    ·1pn74WFkmLPx3gnPhESA&Timestamp=1408704141
         * &instanceIds.0=qcvm12345&instanceIds.1=qcvm56789
         * ****************************************************************************/
        $SigTxt = $HttpMethod.$FullHttpUrl."?";

        $isFirst = true;
        foreach ($ReqParaArray as $key => $value)
        {
                if (!$isFirst) 
                {
                        $SigTxt = $SigTxt."&";
                }
                $isFirst= false;

                /*拼接签名原文时，如果参数名称中携带_，需要替换成.*/
                if(strpos($key, '_'))
                {
                        $key = str_replace('_', '.', $key);
                }

                $SigTxt=$SigTxt.$key."=".$value;
        }

        /*********************根据签名原文字符串 $SigTxt，生成签名 Signature******************/
        $Signature = base64_encode(hash_hmac('sha1', $SigTxt, $secretKey, true));


        /***************拼接请求串,对于请求参数及签名，需要进行urlencode编码********************/
        $Req = "Signature=".urlencode($Signature);
        foreach ($ReqParaArray as $key => $value)
        {
                $Req=$Req."&".$key."=".urlencode($value);
        }

        /*********************************发送请求********************************/
        if($HttpMethod === 'GET')
        {
                if($isHttps === true)
                {
                        $Req="https://".$FullHttpUrl."?".$Req;
                }
                else
                {
                        $Req="http://".$FullHttpUrl."?".$Req;
                }

                $Rsp = file_get_contents($Req);

        }
        else
        {
                if($isHttps === true)
                {
                        $Rsp= SendPost("https://".$FullHttpUrl,$Req,$isHttps);
                }
                else
                {
                        $Rsp= SendPost("http://".$FullHttpUrl,$Req,$isHttps);
                }
        }

        var_export(json_decode($Rsp,true));
}

function SendPost($FullHttpUrl, $Req, $isHttps)
{

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $Req);

        curl_setopt($ch, CURLOPT_URL, $FullHttpUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        if ($isHttps === true) {
                curl_setopt($ch, CURLOPT_SSL_VERIFYPEER,  false);
                curl_setopt($ch, CURLOPT_SSL_VERIFYHOST,  false);
        }

        $result = curl_exec($ch);

        return $result;
}
