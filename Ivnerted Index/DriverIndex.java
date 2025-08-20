
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;                   // package for used in hadoop

import java.sql.Driver;

public class DriverIndex {
    public static void main(String[] args) throws Exception{
        if (args.length != 2){
            System.err.println("Usage IndexDriver <input_dir> <output_dir>");             // for input path and output path
            System.exit(2);
        }
        String input =args[0];
        String output =args[1];

        Configuration conf = new Configuration();            //new object of configuration
        FileSystem fs = FileSystem.get(conf);



        boolean exists =fs.exists(new Path(output));         // To avoid output error (using the same dir)
        if(exists){
            fs.delete(new Path(output),true);
        }
        Job job = Job.getInstance(conf);                      // new object of job to make your task

        job.setJarByClass(DriverIndex.class);
        job.setMapperClass(MapperIndex.class);
        job.setCombinerClass(CombinerIndex.class);
        job.setReducerClass(ReducerIndex.class);               // set your classes map reduce combiner main

        job.setOutputKeyClass(Text.class);                    // bigdata	file2:2;file3:2;file1:1;
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job,new Path(input));      // path for input and output
        FileOutputFormat.setOutputPath(job,new Path(output));

        System.exit(job.waitForCompletion(true)?0:1);   // for validate
    }
}