import java.util.*;
import java.io.*;
 
public class sol2 
{
    //Ordlista som innehåller alla ord.
        static HashSet <String> ordlista = new HashSet <String> ();
 
        //Orka fånga exceptions. Vi är lata och säkra på vår sak.
        public static void main(String [] klein) throws FileNotFoundException
        {
                //Vi ska läsa av filen bokstav.dat i mappen/katalogen data.
                Scanner scan = new Scanner(System.in);
 
                //Antalet ord.
                int N = scan.nextInt();
 
                //Lagrar alla ord. (Egentligen onödigt.)
                String [] ord = new String [N];
 
                //Vårt sökträd.
                MyTree tree = new MyTree();
 
                //Läser in alla ord.
                for(int i = 0; i<N; i++)
                {
                        //Läser in ordet.
                        ord[i] = scan.next();
 
                        //Lägger till det i ordlistan.
                        ordlista.add(ord[i]);
 
                        //Bygger på sökträdet med det här ordet.
                        //D.v.s. lägger till alla substrings som ges av ordet.
                        for(int j = 1; j<=ord[i].length(); j++)
                        {
                                tree.add(ord[i].substring(0,j));
                        }
                }
 
                //Skriver ut alla säkra bokstäver.
                System.out.println(tree.getSafe());
        }
 
        //Hemmagjord klass som beskriver ett "träd" i denna uppgift.
        private static class MyTree
        {
                //Roten har "level" 0.
                private int root = 0;
 
                //Alla olika första bokstäver man får säga.
                private ArrayList <BNode> children;
 
                //Vilka substrings som redan finns i trädet.
                HashSet <String> used = new HashSet <String> ();
 
                //Skapar trädet.
                public MyTree()
                {
                        children = new ArrayList <BNode> ();
                }
 
                //Lägger till en nod i trädet.
                //I vårt fall en del av ett ord (en substring).
                public void add(String s)
                {
                        //Om den delen redan fanns, så behöver vi inte lägga till den.
                        if(!used.add(s)) return;
 
                        //Om det bara är en bokstav ska den växa ut ifrån roten.
                        if(s.length()==root+1)
                        {
                                children.add(new BNode(s));
                        }
                        else //Annars läggs den till på rätt plats.
                        {
                                //Går igenom alla noder till denna nod (roten).
                                for(int i = 0; i<children.size(); i++)
                                {
                                        BNode parent = children.get(i);
 
                                        //Om den här noden är förälder till den
                                        // noden vi tänker lägga till, så ska vår
                                        // nod placeras någonstans under den.
                                        if(parent.isParent(s))
                                        {
                                                parent.add(s);
                                                break;
                                        }
                                }
                        }
                }
 
                //Retunerar alla säkra bokstäver.
                public String getSafe()
                {
                        String safe = "";
 
                        //Går igenom alla noder (första bokstäver).
                        for(BNode node : children)
                        {
                                //Om den är säker.
                                if(node.isSafe())
                                {
                                        safe += " " + node.getWord();
                                }
                        }
 
                        return safe;
                }
 
                //Hemmagjord klass som beksriver en nod i trädet.
                private class BNode
                {
                        //Vilken nivå vi är i. (Hur många bokstäver delordet innehåller.)
                        private int level;
 
                        //Själva (del)ordet.
                        private String word;
 
                        //Alla delord som kan nås från detta ord.
                        private ArrayList <BNode> nodes;
 
                        //Skapar noden.
                        public BNode(String s)
                        {
                                word = s;
                                level = s.length();
                                nodes = new ArrayList <BNode> ();
                        }
 
                        //Retunerar huruvida det här ordet är säkert för Anna.
                        //true = vinst för Anna. false = vinst för Bosse.
                        public boolean isSafe()
                        {
                                //Om ordlistan innehåller det här ordet.
                                if(ordlista.contains(word))
                                {
                                        //Om det är Bosse som tvingas säga detta ord, så vinner Anna.
                                        //Annars vinner Bosse (det är Anna som måste säga ordet).
                                        //Kollar om ordet har jämnt antal bokstäver, för då är det
                                        // Bosses ord att säga.
                                        if(level%2==0) return true;
                                        else return false;
                                }
                                else
                                {
                                        //Om Anna ska säga detta ord.
                                        if(level%2==1)
                                        {
                                                //Så är ordet säkert om alla ord som kan nås från detta
                                                // ord också är säkra.
                                                for(BNode node : nodes)
                                                {
                                                        //Om det finns ett ord som kan nås som är osäkert, så
                                                        // är detta (del)ord också osäkert, eftersom Bosse
                                                        // alltid kommer välja det ord som är osäkert för Anna.
                                                        if(!node.isSafe()) return false;
                                                }
 
                                                return true;
                                        }
                                        else //Om Bosse ska säga detta ord.
                                        {
                                                //Så är detta ord säkert (för Anna) om det finns något ord
                                                // som kan nås från detta (del)ord som också är säkert.
                                                for(BNode node : nodes)
                                                {
                                                        if(node.isSafe()) return true;
                                                }
 
                                                return false;
                                        }
                                }
                        }
 
                        //Lägger till en nod någonstans under denna nod.
                        public void add(String s)
                        {
                                //Om (del)ordet bara är en bokstav längre än detta så ska
                                // ordet länkas till från denna nivå (detta ord).
                                if(s.length()==level+1)
                                {
                                        nodes.add(new BNode(s));
                                }
                                else
                                {
                                        //Annars skickar vi vidare ordet till någon mer
                                        // närstående förälder.
                                        for(int i = 0; i<nodes.size(); i++)
                                        {
                                                BNode parent = nodes.get(i);
 
                                                if(parent.isParent(s))
                                                {
                                                        parent.add(s);
                                                        break;
                                                }
                                        }
                                }
                        }
 
                        //Retunerar huruvida detta ord är förälder tillden givna ordet (s).
                        public boolean isParent(String s)
                        {
                                //Det är vi om ordet börjar med vårt ord.
                                return s.startsWith(word);
                        }
 
                        //Retunerar denna nods ord. (Behövs när trädet ska accessa alla level 1 ord.)
                        public String getWord()
                        {
                                return word;
                        }
                }
        }
        /*** MyTree Ends ***/
}
