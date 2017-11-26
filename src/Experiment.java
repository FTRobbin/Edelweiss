/**
 * Created by RobbinNi on 26/11/2017.
 */
public class Experiment {

    private final ExperimentSetting setting;

    private ExpState state;

    private enum ExpState {
        Ready, Finished;
    }

    private final Controller c;

    public Experiment(ExperimentSetting setting) {
        this.setting = setting;
        this.c = new Controller(setting);
        this.state = ExpState.Ready;
    }

    public void run() {
        if (state == ExpState.Ready) {
            c.run();
            state = ExpState.Finished;
        } else {
            throw new RuntimeException();
        }
    }

    public void report() {
        if (state == ExpState.Finished) {
            c.report();
        } else {
            throw new RuntimeException();
        }
    }

}
