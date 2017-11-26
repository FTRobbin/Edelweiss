/**
 * Created by RobbinNi on 26/11/2017.
 */
public class Main {

    static public void main(String[] args) {
        //Get parameters
        int n = 10, leaderInput = 1;
        ExperimentSetting setting = new ExperimentSetting(n, leaderInput);
        Experiment e = new Experiment(setting);
        e.run();
        e.report();
    }
}
