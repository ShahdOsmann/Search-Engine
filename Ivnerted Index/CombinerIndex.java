
import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class CombinerIndex extends Reducer<Text,Text,Text,Text> {
    private final Text fileAtWordFreqValue = new Text();

    @Override
    protected void reduce(Text key,java.lang.Iterable<Text> values, Context context) throws IOException, InterruptedException{
        int sum = 0;
        //<word@filename , 1>   ==> word ,  filename:sum
        for (Text value:values){                                            // sum=3
            sum += Integer.parseInt(value.toString());
        }

        int splitIndex = key.toString().indexOf("@");

        fileAtWordFreqValue.set(key.toString().substring(splitIndex+1)+":"+sum);
        key.set(key.toString().substring(0,splitIndex));
        context.write(key,fileAtWordFreqValue);
    }
}