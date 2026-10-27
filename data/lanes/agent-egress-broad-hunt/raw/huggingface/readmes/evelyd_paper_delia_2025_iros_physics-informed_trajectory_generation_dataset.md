---
license: bsd-3-clause
---


<h1 align="center">
Stabilizing Humanoid Robot Trajectory Generation via Physics-Informed Learning and Control-Informed Steering
</h1>

<div align="center">
Evelyn D'Elia, Paolo Maria Viceconte, Lorenzo Rapetti, Diego Ferigo, Giulio Romualdi, Giuseppe L'Erario, Raffaello Camoriano, and Daniele Pucci <br> <br>
</div>

<br>

<div align="center">
Submitted to the 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS).
</div>

<section>
<h2>📂 Dataset</h2>

<p>
The dataset is organized in folders. The layout is explained below.
</p>
<ul>
<li>
The <code>mocap/D2</code> folder contains the raw motion capture data, acquired via a human using the Xsens motion tracking suit. Within <code>D2</code> there are 5 subfolders for each data subset: forward, backward, side, diagonal, and mixed walking. each subfolder contains a <code>log</code> file which can be retargeted onto the robot.
</li>
<li>
The <code>retargeted_mocap</code> folder contains the text files of the retargeted mocap data, in both original (<code>D2</code>) and mirrored (<code>D2_mirrored</code>) form.
</li>
<li>
The <code>IO_features</code> folder contains the text files of the extracted features (data and labels) to be used in training. There are 4 subfolders which correspond to the original and mirrored inputs and the original and mirrored outputs.
</li>
<li>
The <code>onnx</code> folder contains the onnx files corresponding to trained models from each PI loss value as well as from the original ADHERENT framework.
</li>
<li>
The <code>reproduce_plots</code> folder contains <code>.mat</code> files with all the data needed to reproduce the selected plots.
</li>
</ul>
</section>