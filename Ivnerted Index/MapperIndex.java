
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
public class MapperIndex extends Mapper<LongWritable,Text,Text,Text> {                   // hdfs file1.txt 1
    private Text keyInfo = new Text();                                   // word@filename
    private Text valueInfo = new Text();                                 // "1"

    private FileSplit split;

    protected void map(LongWritable key,Text value,Mapper<LongWritable,Text,Text,Text>.Context context) throws  IOException, InterruptedException{
        this.split = (FileSplit)context.getInputSplit();

        StringTokenizer tokenizer = new StringTokenizer(value.toString());

        while (tokenizer.hasMoreTokens()){
            String filename = this.split.getPath().getName().split("\\.")[0];

            this.keyInfo.set(tokenizer.nextToken()+"@"+filename);

            this.valueInfo.set("1");
            //<word@filename , 1>
            context.write(this.keyInfo, this.valueInfo);
        }
    }
}