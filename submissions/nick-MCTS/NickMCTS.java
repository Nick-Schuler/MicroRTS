package NickMCTS;

import ai.mcts.naivemcts.NaiveMCTS;
import ai.core.AI;
import rts.units.UnitTypeTable;
import ai.evaluation.LanchesterEvaluationFunction;
import ai.abstraction.WorkerRush;

// Your Evaluation Class
class MyEvaluation extends LanchesterEvaluationFunction {
    private UnitTypeTable utt;

    public MyEvaluation(UnitTypeTable utt) {
        this.utt = utt;
    }

    @Override
    public float evaluate(int maxplayer, int minplayer, rts.GameState gs) {
        float score = super.evaluate(maxplayer, minplayer, gs);
        float threatPenalty = calculateThreat(maxplayer, gs);
        
        float carryingBonus = 0;
        for (rts.units.Unit u : gs.getUnits()) {
            if (u.getPlayer() == maxplayer && u.getResources() > 0) {
                carryingBonus += 0.2f;
            }
        }
        return score - threatPenalty + carryingBonus;
    }

    private float calculateThreat(int player, rts.GameState gs) {
        float threatPenalty = 0.0f;
        rts.PhysicalGameState pgs = gs.getPhysicalGameState();
        int enemy = 1 - player;
        for (rts.units.Unit myUnit : pgs.getUnits()) {
            if (myUnit.getPlayer() == player && myUnit.getType().name.equals("Base")) {
                for (rts.units.Unit enemyUnit : pgs.getUnits()) {
                    if (enemyUnit.getPlayer() == enemy) {
                        int dist = Math.abs(myUnit.getX() - enemyUnit.getX()) + 
                                   Math.abs(myUnit.getY() - enemyUnit.getY());
                        if (dist < 8) {
                            threatPenalty += (8 - dist) * 0.1f;
                        }
                    }
                }
            }
        }
        return threatPenalty;
    }
}

// Your AI Class
public class NickMCTS extends NaiveMCTS {

    private UnitTypeTable utt;

    // Main Constructor
    public NickMCTS(UnitTypeTable utt) {
        super(
            100, -1, 100, 10,
            0.3f, 1.0f,
            0.0f, 1.0f,
            0.4f, 1.0f,
            new WorkerRush(utt), 
            new MyEvaluation(utt), 
            true
        );
        this.utt = utt; // IMPORTANT: Save the table for cloning!
    }

    // Default Constructor (Required for many Tournament GUIs)
    public NickMCTS() {
        this(new UnitTypeTable());
    }

    @Override
    public AI clone() {
        return new NickMCTS(utt);
    }
}
