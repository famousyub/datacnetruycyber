


class Test {


      public static void main(String[] args) {
        

             String name="10_TXTX__2412_MCS0__BW20_ANT1";
             
            

             Integer indexof_ =  name.indexOf("TXTX" , 0);

             System.out.println(indexof_);
             String []  names = name.split("_");
             String namefinal ="";
             String t =  "" ;
             for (String n : names){
                

                 if (n.indexOf("TXTX") != -1){
                         n.replace(n, "TX");
                         
                         n = String.format("%s", n.substring(0 ,  2));
                         

                 }

                
                t +=    n ;

                        

                namefinal = String.format("%s", t);
              
                t +="_";


             }
             namefinal.replace("__", "_");
             System.out.println(namefinal + "\n");
             

             if (indexof_ != -1){
                   name.replace(name.subSequence(indexof_,"TXTX".length() ), "TX");
                   
         
                   System.out.println(name.substring(indexof_, "TXTX".length()));
                   

                   System.out.println(name);

             }


      }
}

