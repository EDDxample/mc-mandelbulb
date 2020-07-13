package net.fabricmc.example;

import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.dimension.DimensionType;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;

import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.builder.LiteralArgumentBuilder;
import net.minecraft.server.command.ServerCommandSource;

import static net.minecraft.server.command.CommandManager.literal;

/**

@Mixin(CommandManager.class)
public class ExampleMixin {

	@Shadow
	@Final
	private CommandDispatcher<ServerCommandSource> dispatcher;

	@Inject(method = "<init>", at = @At("RETURN"))
	private void onRegister(boolean boolean_1, CallbackInfo ci) {
		ExampleMod.register(dispatcher);
	}
}

*/

public class ExampleMod {
	static int step, skip = 1;
	static byte[] data;

	private static final BlockState[] colors = {
		Blocks.LIGHT_BLUE_CONCRETE.getDefaultState(),
		Blocks.CYAN_CONCRETE.getDefaultState(),
		Blocks.BLUE_CONCRETE.getDefaultState(),
		Blocks.GREEN_CONCRETE.getDefaultState(),
		Blocks.LIME_CONCRETE.getDefaultState(),
		Blocks.YELLOW_CONCRETE.getDefaultState(),
		Blocks.ORANGE_CONCRETE.getDefaultState(),
		Blocks.BROWN_CONCRETE.getDefaultState(),
		Blocks.RED_CONCRETE.getDefaultState(),
		Blocks.PINK_CONCRETE.getDefaultState(),
		Blocks.MAGENTA_CONCRETE.getDefaultState(),
		Blocks.PURPLE_CONCRETE.getDefaultState(),
		Blocks.BLACK_CONCRETE.getDefaultState(),
		Blocks.GRAY_CONCRETE.getDefaultState(),
		Blocks.LIGHT_GRAY_CONCRETE.getDefaultState(),
		Blocks.WHITE_CONCRETE.getDefaultState()
	};

	private static BlockState getColor(int n) {
		int larr = colors.length;
		int i = n % (larr * 2 - 2);
		if (i < larr) return colors[i];
		i %= larr;
		return colors[larr - i - 2];
	}

	public static void register(CommandDispatcher<ServerCommandSource> dispatcher) {
		LiteralArgumentBuilder<ServerCommandSource> command2 = literal("step")
				.executes(c -> {
					MinecraftServer server = c.getSource().getMinecraftServer();
					ServerWorld w = server.getWorld(DimensionType.OVERWORLD);

					while (skip > 0 && step < data.length) {
						int x = data[step++];
						int y = data[step++] + 128;
						int z = data[step++];

						int r = data[step++];
						w.setBlockState(new BlockPos(x,y, z) , getColor(r));
						skip--;
					}
					skip = 1;

					return 1;

				}).then(literal("reset").executes(c -> {
					skip = 1;
					step = 0;
					return 1;
				}))
				.then(literal("skip").executes(c -> {
					skip = 30;
					return 1;
				}));

		LiteralArgumentBuilder<ServerCommandSource> command = literal("mandel")
				.executes(c -> {
					MinecraftServer server = c.getSource().getMinecraftServer();
					ServerWorld w = server.getWorld(DimensionType.OVERWORLD);
					try {
						File f = new File("mandelbulb.bin");

						byte[] data = FileUtils.readFileToByteArray(f);
						ByteBuffer bb = ByteBuffer.wrap(data);

						while (bb.hasRemaining()) {
							int r = bb.getInt();
							w.setBlockState(new BlockPos(bb.getInt(), bb.getInt() + 127, bb.getInt()), getColor(r));
						}

					} catch	(Exception e) {
						e.printStackTrace();
					}

					return 1;
				});
		dispatcher.register(command);
		dispatcher.register(command2);
	}

	static {
		try {
			data = FileUtils.readFileToByteArray(new File("mandelbulb.bin")); // /.minecraft/mandelbulb.bin
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}