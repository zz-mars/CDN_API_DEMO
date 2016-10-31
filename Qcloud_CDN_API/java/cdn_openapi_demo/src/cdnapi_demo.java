import java.util.TreeMap;
import Json.*;
import Utilities.*;


public class cdnapi_demo {
    public static void main(String[] args) {
    	
    	//params
    	String serverHost = "cdn.api.qcloud.com";
    	String serverUri = "/v2/index.php";
    	String secretId = "AKIDxUCsd01oB7B9OiquUFihD8hlRhftKmXr";
    	String secretKey = "zI4aKkKA7GxC1pMxSABTbmCy7GbwJhPJ";
    	String requestMethod = "GET";
    	String defaultRegion = "gz";
    	String action="RefreshCdnUrl";
    	
    	/*add interface params,e.g.DescribeHosts*/	
    	TreeMap<String, Object> params = new TreeMap<String, Object>();
    	params.put("urls.0","http://haowentang.att.oa.com/test.php");
    	params.put("urls.1","http://haowentang.att.oa.com/test2.php");
		if(params == null)
			params = new TreeMap<String, Object>();
		action = cdnapi_demo.ucFirst(action);
		params.put("Action", action);
        System.out.println(params);

		try{
			String response = Request.send(params, secretId, secretKey, requestMethod, serverHost, serverUri, null);
            /*use generateUrl to get url*/
            String url = Request.generateUrl(params, secretId, secretKey, requestMethod, serverHost, serverUri);
            System.out.println("correct request url:["+url+"]");
			JSONObject result = new JSONObject(response);
            System.out.println(result);
            
		}
		catch (Exception e){
			System.out.println("error..." + e.getMessage());
		}
		
    }
    private static String ucFirst(String word){
        return word.replaceFirst(word.substring(0, 1), 
                word.substring(0, 1).toUpperCase());
    }  
}
